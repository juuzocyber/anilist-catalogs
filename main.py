"""
AniList Catalogs — FastAPI entry point.
"""

import logging
import random
import secrets
import time
from contextlib import asynccontextmanager

import httpx
import pydantic

from fastapi import FastAPI, HTTPException, Request, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

import anilist
from cache import cache, TTL, SESSION_TTL
from config import decode_config, DEFAULT_CONFIG, DEFAULT_CONFIG_TOKEN, CURRENT_YEARS
from configure import CONFIGURE_HTML
from crypto import encrypt, decrypt
from cryptography.fernet import InvalidToken
from manifest import MANIFEST
from settings import HOST, PORT, ANILIST_CLIENT_ID, ANILIST_CLIENT_SECRET, ANILIST_REDIRECT_URI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)
PER_PAGE = 30

PRESET_HANDLERS = {
    "anilist-popular-season": anilist.get_popular_season,
    "anilist-airing-week":    anilist.get_airing_week,
    "anilist-trending":       anilist.get_trending,
    "anilist-top-rated":      anilist.get_top_rated,
}

def _skip_to_page(skip): return max(1, skip // PER_PAGE + 1)

def _parse_config_segment(segment: str) -> tuple[str, str | None]:
    """Split a URL path segment into (config_token, session_key | None).

    The segment format is "{config_token}~{session_key}" when authenticated,
    or just "{config_token}" for unauthenticated / public manifests.
    '~' is used as the separator because it is unreserved in RFC 3986
    and never appears in base64url output.
    """
    if "~" in segment:
        config_token, session_key = segment.split("~", 1)
        return config_token, session_key
    return segment, None

def _build_manifest(config):
    catalogs = []
    for cat in config.get("catalogs", []):
        catalogs.append({"type": "series", "id": cat["id"], "name": cat["name"], "extra": [{"name": "skip", "isRequired": False}]})
    m = dict(MANIFEST)
    m["catalogs"] = catalogs
    m["behaviorHints"] = {**m.get("behaviorHints", {}), "configurable": True, "configurationRequired": False}
    return m

async def _fetch_catalog(catalog_id, catalog_config, page, encrypted_token: str | None = None):
    cache_key = f"catalog:{catalog_id}:page:{page}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    if catalog_id in PRESET_HANDLERS:
        metas = await PRESET_HANDLERS[catalog_id](page=page, per_page=PER_PAGE)
        ttl = TTL.get(catalog_id, 15 * 60)
    elif catalog_config.get("type") == "custom":
        metas = await anilist.get_custom(catalog_config.get("filters", {}), page=page, per_page=PER_PAGE)
        ttl = 30 * 60
    elif catalog_config.get("type") == "watching":
        if not encrypted_token:
            raise HTTPException(status_code=401, detail="Authentication required for watching list.")
        try:
            raw_token = decrypt(encrypted_token)
        except InvalidToken:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        viewer = await anilist.get_viewer(raw_token)
        # Do not cache user-specific lists — they change frequently.
        list_status = catalog_config.get("listStatus")
        if list_status == "FAVOURITES":
            return await anilist.get_favourites(raw_token, viewer["id"])
        return await anilist.get_watching_list(raw_token, viewer["id"], list_status or "CURRENT")
    else:
        raise HTTPException(status_code=404, detail=f"Unknown catalog: {catalog_id}")
    cache.set(cache_key, metas, ttl)
    return metas

@asynccontextmanager
async def lifespan(app):
    from settings import SECRET_KEY as _sk
    if not _sk:
        raise RuntimeError(
            "SECRET_KEY is not set. Generate one with:\n"
            "  python -c \"import secrets; print(secrets.token_hex(32))\"\n"
            "and add it to your .env file."
        )
    logger.info("AniList add-on starting on %s:%d — configure at /configure", HOST, PORT)
    yield

app = FastAPI(title="AniList Catalogs", version=MANIFEST["version"], lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

@app.get("/", include_in_schema=False)
async def root(): return RedirectResponse(url="/configure")

@app.get("/configure", response_class=HTMLResponse)
async def configure_page():
    year_options = "\n".join(f'<option value="{y}">{y}</option>' for y in CURRENT_YEARS)
    return HTMLResponse(CONFIGURE_HTML.replace("__YEAR_OPTIONS__", year_options))

@app.post("/anilist-proxy")
async def anilist_proxy(request: Request):
    # Enforce a body size limit to prevent resource exhaustion.
    body = await request.body()
    if len(body) > 16_384:
        raise HTTPException(status_code=413, detail="Request body too large.")

    # Validate the body is a well-formed GraphQL request: must be a JSON object
    # with a string `query` field. Mutations and introspection queries are blocked
    # since the configure page only needs read queries.
    import json as _json
    try:
        payload = _json.loads(body)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body.")

    if not isinstance(payload, dict) or not isinstance(payload.get("query"), str):
        raise HTTPException(status_code=400, detail="Missing or invalid 'query' field.")

    query_text = payload["query"].strip().lstrip("{")
    if query_text.lower().startswith("mutation"):
        raise HTTPException(status_code=403, detail="Mutations are not permitted.")
    if "__schema" in query_text or "__type" in query_text:
        raise HTTPException(status_code=403, detail="Introspection queries are not permitted.")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://graphql.anilist.co",
            content=body,
            headers={"Content-Type": "application/json"},
            timeout=15,
        )
    return JSONResponse(content=resp.json(), status_code=resp.status_code)

@app.get("/health")
async def health(): return {"status": "ok", "cache_entries": len(cache)}

# ── OAuth 2.0 ─────────────────────────────────────────────────────────────────

_ANILIST_AUTH_URL  = "https://anilist.co/api/v2/oauth/authorize"
_ANILIST_TOKEN_URL = "https://anilist.co/api/v2/oauth/token"

@app.get("/oauth/login", include_in_schema=False)
async def oauth_login():
    if not ANILIST_CLIENT_ID or not ANILIST_REDIRECT_URI:
        raise HTTPException(status_code=500, detail="OAuth is not configured on this server.")
    from urllib.parse import urlencode
    state = secrets.token_urlsafe(32)
    params = urlencode({
        "client_id":     ANILIST_CLIENT_ID,
        "redirect_uri":  ANILIST_REDIRECT_URI,
        "response_type": "code",
        "state":         state,
    })
    response = RedirectResponse(url=f"{_ANILIST_AUTH_URL}?{params}")
    # Store state in a short-lived HttpOnly cookie so the callback can verify it.
    response.set_cookie(
        "oauth_state", state,
        httponly=True, samesite="lax", max_age=600, secure=False,
    )
    return response


@app.get("/oauth/callback", include_in_schema=False)
async def oauth_callback(
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    oauth_state: str | None = Cookie(default=None),
):
    if error or not code:
        logger.warning("OAuth callback received without a code (error=%s)", error)
        return RedirectResponse(url="/configure?error=auth_failed")

    # Verify state to prevent CSRF.
    if not state or not oauth_state or not secrets.compare_digest(state, oauth_state):
        logger.warning("OAuth callback state mismatch — possible CSRF attempt")
        response = RedirectResponse(url="/configure?error=auth_failed")
        response.delete_cookie("oauth_state")
        return response

    payload = {
        "grant_type":    "authorization_code",
        "client_id":     ANILIST_CLIENT_ID,
        "client_secret": ANILIST_CLIENT_SECRET,
        "redirect_uri":  ANILIST_REDIRECT_URI,
        "code":          code,
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                _ANILIST_TOKEN_URL,
                json=payload,
                headers={"Accept": "application/json"},
                timeout=15,
            )
        if resp.status_code != 200:
            logger.error("AniList token exchange failed: HTTP %d", resp.status_code)
            return RedirectResponse(url="/configure?error=auth_failed")

        access_token = resp.json().get("access_token")
        if not access_token:
            logger.error("AniList token exchange returned no access_token")
            return RedirectResponse(url="/configure?error=auth_failed")

    except Exception as exc:
        logger.error("AniList token exchange error: %s", exc)
        response = RedirectResponse(url="/configure?error=auth_failed")
        response.delete_cookie("oauth_state")
        return response

    encrypted = encrypt(access_token)
    # Store the encrypted token server-side and hand the client a short session key.
    # This keeps the full encrypted token out of the manifest URL entirely.
    # Losing the session (server restart, TTL expiry) only requires re-authentication —
    # no user data is lost.
    session_key = secrets.token_urlsafe(16)  # 22 URL-safe characters, 128 bits of entropy
    cache.set(f"session:{session_key}", encrypted, SESSION_TTL)
    # Do not log the raw access_token — only the encrypted form is safe to emit.
    logger.info("OAuth login successful; session key stored, redirecting to /configure")
    response = RedirectResponse(url=f"/configure?s={session_key}")
    response.delete_cookie("oauth_state")
    return response


@app.get("/oauth/logout", include_in_schema=False)
async def oauth_logout():
    return RedirectResponse(url="/configure")

# ── Authenticated user API ────────────────────────────────────────────────────

# Simple fixed-window per-IP rate limiter for session-keyed endpoints.
# Keeps one (window_start, count) entry per IP; resets when the window expires.
_session_rate: dict[str, tuple[float, int]] = {}
_SESSION_RATE_WINDOW = 60   # seconds per window
_SESSION_RATE_MAX    = 20   # max requests per IP per window

def _check_session_rate_limit(ip: str) -> bool:
    now = time.monotonic()
    entry = _session_rate.get(ip)
    if entry is None or now - entry[0] >= _SESSION_RATE_WINDOW:
        _session_rate[ip] = (now, 1)
        return True
    if entry[1] >= _SESSION_RATE_MAX:
        return False
    _session_rate[ip] = (entry[0], entry[1] + 1)
    return True

_AUTH_401 = {"detail": "Session not found or expired."}

def _resolve_session(session_key: str) -> str:
    """Look up and decrypt a session token. Raises 401 with a uniform message on any failure."""
    encrypted = cache.get(f"session:{session_key}")
    if not encrypted:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])
    try:
        return decrypt(encrypted)
    except InvalidToken:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])

class _SessionBody(pydantic.BaseModel):
    session: str

_VALID_LIST_STATUSES = {"CURRENT", "PLANNING", "COMPLETED", "PAUSED", "DROPPED", "REPEATING", "FAVOURITES"}

class _PreviewWatchingBody(pydantic.BaseModel):
    session: str
    list_status: str

@app.post("/api/preview-watching")
async def api_preview_watching(request: Request, body: _PreviewWatchingBody):
    """Return the authenticated user's watching list or favourites for the configure UI preview.

    Uses a short-lived session key (never the raw AniList token). Rate-limited
    per IP to prevent session key enumeration.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")
    if body.list_status not in _VALID_LIST_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid list_status.")
    raw_token = _resolve_session(body.session)
    try:
        viewer = await anilist.get_viewer(raw_token)
        if body.list_status == "FAVOURITES":
            media = await anilist.get_favourites(raw_token, viewer["id"], raw=True)
        else:
            media = await anilist.get_watching_list(raw_token, viewer["id"], body.list_status, raw=True)
    except Exception as exc:
        logger.error("preview_watching failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch list from AniList.")
    return {"media": media}

@app.post("/api/me")
async def api_me(request: Request, body: _SessionBody):
    """Return the authenticated user's display name and avatar URL.

    Accepts a short session key in the POST body. The key is looked up in the
    server-side session cache to retrieve the encrypted AniList token — the
    token itself never travels to the client after the initial OAuth exchange.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")
    raw_token = _resolve_session(body.session)
    try:
        viewer = await anilist.get_viewer(raw_token)
    except Exception as exc:
        logger.error("get_viewer failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch user from AniList.")
    return {"name": viewer["name"], "avatar": viewer["avatar"]}

@app.get("/manifest.json")
async def manifest_default(): return JSONResponse(_build_manifest(DEFAULT_CONFIG))

@app.get("/{config_segment}/manifest.json")
async def manifest_configured(config_segment: str):
    config_token, _ = _parse_config_segment(config_segment)
    return JSONResponse(_build_manifest(decode_config(config_token)))

@app.get("/{config_segment}/catalog/{content_type}/{catalog_id}.json")
@app.get("/{config_segment}/catalog/{content_type}/{catalog_id}/skip={skip}.json")
async def catalog_configured(config_segment: str, content_type: str, catalog_id: str, skip: int = 0):
    if content_type != "series":
        raise HTTPException(status_code=404, detail="Unsupported content type")
    config_token, session_key = _parse_config_segment(config_segment)
    config = decode_config(config_token)
    catalog_config = next((c for c in config.get("catalogs", []) if c["id"] == catalog_id), None)
    if catalog_config is None:
        raise HTTPException(status_code=404, detail=f"Catalog not in config: {catalog_id}")
    page = _skip_to_page(skip)
    # Resolve encrypted token: prefer session key (new), fall back to legacy embedded token.
    encrypted_token: str | None = None
    if session_key:
        encrypted_token = cache.get(f"session:{session_key}")
    if not encrypted_token:
        encrypted_token = config.get("token")  # backward compat with old URLs
    try:
        metas = await _fetch_catalog(catalog_id, catalog_config, page, encrypted_token)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Fetch failed for %s: %s", catalog_id, exc)
        raise HTTPException(status_code=502, detail="AniList API error") from exc
    if catalog_config.get("randomize"):
        metas = random.sample(metas, len(metas))
    return JSONResponse({"metas": metas})

@app.get("/{config_segment}/meta/{content_type}/{item_id}.json")
async def meta_configured(config_segment: str, content_type: str, item_id: str):
    config_token, _ = _parse_config_segment(config_segment)
    if content_type != "series":
        raise HTTPException(status_code=404, detail="Unsupported content type")
    if not item_id.startswith("anilist:"):
        raise HTTPException(status_code=404, detail="Unknown ID prefix")
    raw_id = item_id.removeprefix("anilist:")
    if not raw_id.isdigit():
        raise HTTPException(status_code=400, detail="Invalid AniList ID")
    anilist_id = int(raw_id)
    cache_key = f"meta:{anilist_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return JSONResponse({"meta": cached})
    try:
        meta_data = await anilist.get_meta(anilist_id)
    except Exception as exc:
        logger.error("Meta fetch failed for %d: %s", anilist_id, exc)
        raise HTTPException(status_code=502, detail="AniList API error") from exc
    if not meta_data:
        raise HTTPException(status_code=404, detail="Anime not found")
    cache.set(cache_key, meta_data, TTL["meta"])
    return JSONResponse({"meta": meta_data})

@app.get("/catalog/{content_type}/{catalog_id}.json")
@app.get("/catalog/{content_type}/{catalog_id}/skip={skip}.json")
async def catalog_legacy(content_type: str, catalog_id: str, skip: int = 0):
    return await catalog_configured(DEFAULT_CONFIG_TOKEN, content_type, catalog_id, skip)

@app.get("/meta/{content_type}/{item_id}.json")
async def meta_legacy(content_type: str, item_id: str):
    return await meta_configured(DEFAULT_CONFIG_TOKEN, content_type, item_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)
