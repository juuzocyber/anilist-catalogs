"""
AniList Catalogs — FastAPI entry point.
"""

import logging
import random
import secrets
from contextlib import asynccontextmanager

import httpx
import pydantic

from fastapi import FastAPI, HTTPException, Request, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse

import anilist
from cache import cache, TTL
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
        # Do not cache watching lists — they are user-specific and change frequently.
        return await anilist.get_watching_list(raw_token, viewer["id"])
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
    # Do not log the raw access_token — only the encrypted form is safe to emit.
    logger.info("OAuth login successful; token encrypted and forwarded to /configure")
    response = RedirectResponse(url=f"/configure?token={encrypted}")
    response.delete_cookie("oauth_state")
    return response


@app.get("/oauth/logout", include_in_schema=False)
async def oauth_logout():
    return RedirectResponse(url="/configure")

# ── Authenticated user API ────────────────────────────────────────────────────

class _TokenBody(pydantic.BaseModel):
    token: str

@app.post("/api/me")
async def api_me(body: _TokenBody):
    """Return the authenticated user's display name and avatar URL.

    Accepts the encrypted token in the POST body — never as a URL parameter —
    so it does not appear in server access logs or browser history.
    The decrypted bearer token is used only for the AniList request and is
    never included in the response or logs.
    """
    try:
        raw_token = decrypt(body.token)
    except InvalidToken:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    try:
        viewer = await anilist.get_viewer(raw_token)
    except Exception as exc:
        logger.error("get_viewer failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch user from AniList.")
    return {"name": viewer["name"], "avatar": viewer["avatar"]}

@app.get("/manifest.json")
async def manifest_default(): return JSONResponse(_build_manifest(DEFAULT_CONFIG))

@app.get("/{config_token}/manifest.json")
async def manifest_configured(config_token: str):
    return JSONResponse(_build_manifest(decode_config(config_token)))

@app.get("/{config_token}/catalog/{content_type}/{catalog_id}.json")
@app.get("/{config_token}/catalog/{content_type}/{catalog_id}/skip={skip}.json")
async def catalog_configured(config_token: str, content_type: str, catalog_id: str, skip: int = 0):
    if content_type != "series":
        raise HTTPException(status_code=404, detail="Unsupported content type")
    config = decode_config(config_token)
    catalog_config = next((c for c in config.get("catalogs", []) if c["id"] == catalog_id), None)
    if catalog_config is None:
        raise HTTPException(status_code=404, detail=f"Catalog not in config: {catalog_id}")
    page = _skip_to_page(skip)
    try:
        metas = await _fetch_catalog(catalog_id, catalog_config, page, config.get("token"))
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Fetch failed for %s: %s", catalog_id, exc)
        raise HTTPException(status_code=502, detail="AniList API error") from exc
    if catalog_config.get("randomize"):
        metas = random.sample(metas, len(metas))
    return JSONResponse({"metas": metas})

@app.get("/{config_token}/meta/{content_type}/{item_id}.json")
async def meta_configured(config_token: str, content_type: str, item_id: str):
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
