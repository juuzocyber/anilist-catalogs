"""
AniList Catalogs — FastAPI entry point.
"""

import logging
import random
import re
import secrets
import time
from contextlib import asynccontextmanager
from urllib.parse import urlparse

import httpx
import pydantic

from fastapi import FastAPI, HTTPException, Request, Cookie, Response
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import anilist
from cache import cache, TTL, SESSION_TTL
from id_mapper import batch_map_ids, reverse_lookup
from config import decode_config, DEFAULT_CONFIG, DEFAULT_CONFIG_TOKEN, CURRENT_YEARS
from configure import CONFIGURE_HTML
from crypto import encrypt, decrypt
from cryptography.fernet import InvalidToken
from manifest import MANIFEST
from settings import (
    HOST,
    PORT,
    ANILIST_CLIENT_ID,
    ANILIST_CLIENT_SECRET,
    ANILIST_REDIRECT_URI,
    ENABLE_API_DOCS,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)
PER_PAGE = 50

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


def _is_local_host(hostname: str | None) -> bool:
    return hostname in {"localhost", "127.0.0.1", "::1"}


def _oauth_cookie_secure() -> bool:
    parsed = urlparse(ANILIST_REDIRECT_URI or "")
    return parsed.scheme.lower() == "https"


def _is_public_oauth_redirect() -> bool:
    parsed = urlparse(ANILIST_REDIRECT_URI or "")
    return bool(parsed.hostname) and not _is_local_host(parsed.hostname)


def _is_addon_route(path: str) -> bool:
    return (
        path == "/manifest.json"
        or path.startswith("/catalog/")
        or path.startswith("/meta/")
        or path.endswith("/manifest.json")
        or "/catalog/" in path
        or "/meta/" in path
    )


def _apply_addon_cors(response: Response) -> None:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Max-Age"] = "86400"


_request_rate: dict[str, tuple[float, int]] = {}
_RATE_LIMITS = {
    "oauth": (60, 20),
    "api": (60, 60),
    "proxy": (60, 30),
    "addon": (60, 240),
}


def _rate_bucket(path: str) -> str | None:
    if path.startswith("/oauth/"):
        return "oauth"
    if path.startswith("/api/"):
        return "api"
    if path == "/anilist-proxy":
        return "proxy"
    if _is_addon_route(path):
        return "addon"
    return None


def _check_rate_limit(bucket: str, key: str) -> bool:
    now = time.monotonic()
    window, limit = _RATE_LIMITS[bucket]
    cache_key = f"{bucket}:{key}"
    entry = _request_rate.get(cache_key)
    if entry is None or now - entry[0] >= window:
        _request_rate[cache_key] = (now, 1)
        return True
    if entry[1] >= limit:
        return False
    _request_rate[cache_key] = (entry[0], entry[1] + 1)
    return True


def _build_configure_csp(nonce: str) -> str:
    return "; ".join([
        "default-src 'self'",
        f"script-src 'self' 'nonce-{nonce}'",
        f"style-src 'self' 'nonce-{nonce}'",
        "img-src 'self' data: https:",
        "connect-src 'self'",
        "font-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "frame-ancestors 'none'",
        "form-action 'self'",
    ])

async def _fetch_catalog(
    catalog_id,
    catalog_config,
    page,
    encrypted_token: str | None = None,
    session_key: str | None = None,
):
    cache_key = f"catalog:{catalog_id}:page:{page}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    raw_media = None
    ttl = None
    should_cache = True

    if catalog_id in PRESET_HANDLERS:
        raw_media = await PRESET_HANDLERS[catalog_id](page=page, per_page=PER_PAGE)
        ttl = TTL.get(catalog_id, 15 * 60)
    elif catalog_config.get("type") == "custom":
        raw_media = await anilist.get_custom(catalog_config.get("filters", {}), page=page, per_page=PER_PAGE)
        ttl = 30 * 60
    elif catalog_config.get("type") == "watching":
        if not encrypted_token:
            raise HTTPException(status_code=401, detail="Authentication required for watching list.")
        try:
            raw_token = decrypt(encrypted_token)
        except InvalidToken:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        viewer = await anilist.get_viewer(raw_token)
        list_status = catalog_config.get("listStatus")
        if list_status == "FAVOURITES":
            raw_media = await anilist.get_favourites(raw_token, viewer["id"])
        else:
            raw_media = await anilist.get_watching_list(raw_token, viewer["id"], list_status or "CURRENT")
        should_cache = False  # user-specific lists change frequently
    elif catalog_config.get("type") == "ai":
        if not encrypted_token or not session_key:
            raise HTTPException(status_code=401, detail="Authentication required for AI recommendations.")
        try:
            raw_token = decrypt(encrypted_token)
        except InvalidToken:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        or_data = cache.get(f"session_or:{session_key}")
        if not or_data:
            raise HTTPException(status_code=400, detail="OpenRouter API key not configured for this session.")
        try:
            or_key = decrypt(or_data["encrypted_key"])
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired OpenRouter session.")
        model = or_data.get("model", "meta-llama/llama-3.3-70b-instruct")
        ai_cache_key = f"ai_recs:{session_key}:{model}"
        ai_cached = cache.get(ai_cache_key)
        if ai_cached is not None:
            raw_media = ai_cached
        else:
            viewer = await anilist.get_viewer(raw_token)
            raw_media = await anilist.get_ai_recommendations(raw_token, viewer["id"], or_key, model)
            cache.set(ai_cache_key, raw_media, 60 * 60)
        should_cache = False  # AI has its own per-session cache
    else:
        raise HTTPException(status_code=404, detail=f"Unknown catalog: {catalog_id}")

    # Batch-map AniList IDs to TMDB/IMDB via Fribb + Kitsu supplement.
    # Sequels (season.tvdb > 1) are replaced with their S1 base anime.
    id_mapping, replacements = await batch_map_ids(raw_media)

    # Fetch S1 media from AniList for any sequels that need replacing.
    if replacements:
        s1_ids = {s1_aid for s1_aid, _ in replacements.values()}
        # Remove S1 IDs already present in the catalog (no need to fetch)
        existing_ids = {m["id"] for m in raw_media}
        fetch_ids = s1_ids - existing_ids
        s1_media: dict[int, dict] = {}
        if fetch_ids:
            # AniList limits query complexity to 500.  Each aliased Media
            # query costs ~31 points, so we batch in groups of 15.
            id_list = list(fetch_ids)
            S1_BATCH = 15
            for batch_start in range(0, len(id_list), S1_BATCH):
                batch = id_list[batch_start:batch_start + S1_BATCH]
                alias_parts = [
                    f"a{i}: Media(id: {aid}, type: ANIME) {{ {anilist.MEDIA_FIELDS} }}"
                    for i, aid in enumerate(batch)
                ]
                try:
                    data = await anilist._gql("query {\n" + "\n".join(alias_parts) + "\n}", {})
                    for i, aid in enumerate(batch):
                        media = data.get(f"a{i}")
                        if media and isinstance(media, dict) and media.get("id"):
                            s1_media[media["id"]] = media
                except Exception as exc:
                    logger.warning("Failed to fetch S1 media batch: %s", exc)

        # Swap sequels for their S1 in the media list.
        seen_s1: set[int] = set()
        result_media = []
        for m in raw_media:
            aid = m["id"]
            if aid in replacements:
                s1_aid, s1_ext = replacements[aid]
                if s1_aid in seen_s1:
                    continue  # S1 already in catalog (from another sequel or directly)
                seen_s1.add(s1_aid)
                if s1_aid in existing_ids:
                    continue  # S1 is already in raw_media, skip the sequel slot
                if s1_aid in s1_media:
                    s1_m = s1_media[s1_aid]
                    id_mapping[s1_aid] = s1_ext
                    result_media.append(s1_m)
                    continue
                # Fetch failed — keep sequel as anilist: fallback
            result_media.append(m)
        raw_media = result_media

    metas = [
        anilist._media_to_meta(m, id_override=id_mapping.get(m["id"]))
        for m in raw_media
    ]

    if should_cache and ttl:
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
    if any(not value for value in (ANILIST_CLIENT_ID, ANILIST_CLIENT_SECRET, ANILIST_REDIRECT_URI)):
        logger.warning(
            "AniList OAuth is partially configured. client_id=%s client_secret=%s redirect_uri=%s",
            bool(ANILIST_CLIENT_ID),
            bool(ANILIST_CLIENT_SECRET),
            bool(ANILIST_REDIRECT_URI),
        )
    else:
        logger.info("AniList OAuth redirect URI configured as %s", ANILIST_REDIRECT_URI)
        if not ANILIST_REDIRECT_URI.endswith("/oauth/callback"):
            logger.warning(
                "AniList redirect URI looks suspicious: %s (expected to end with /oauth/callback)",
                ANILIST_REDIRECT_URI,
            )
        if _is_public_oauth_redirect() and not _oauth_cookie_secure():
            logger.warning(
                "AniList OAuth redirect URI is not HTTPS for a non-local deployment: %s",
                ANILIST_REDIRECT_URI,
            )
    logger.info("AniList add-on starting on %s:%d — configure at /configure", HOST, PORT)
    yield

app = FastAPI(
    title="AniList Catalogs",
    version=MANIFEST["version"],
    lifespan=lifespan,
    docs_url="/docs" if ENABLE_API_DOCS else None,
    redoc_url="/redoc" if ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if ENABLE_API_DOCS else None,
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    path = request.url.path
    request.state.csp_nonce = secrets.token_urlsafe(16)

    if request.method == "OPTIONS":
        if _is_addon_route(path):
            response = Response(status_code=204)
            _apply_addon_cors(response)
            return response
        return Response(status_code=405)

    bucket = _rate_bucket(path)
    ip = request.client.host if request.client and request.client.host else "unknown"
    if bucket and not _check_rate_limit(bucket, ip):
        return JSONResponse(status_code=429, content={"detail": "Too many requests."})

    response = await call_next(request)
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")

    if path == "/configure":
        response.headers["Content-Security-Policy"] = _build_configure_csp(request.state.csp_nonce)
        response.headers["Cache-Control"] = "no-store"
    elif path.startswith("/oauth/") or path.startswith("/api/") or path == "/anilist-proxy":
        response.headers["Cache-Control"] = "no-store"

    if _is_addon_route(path):
        _apply_addon_cors(response)

    return response

@app.get("/", include_in_schema=False)
async def root(): return RedirectResponse(url="/configure")

@app.get("/configure", response_class=HTMLResponse)
async def configure_page(request: Request):
    year_options = "\n".join(f'<option value="{y}">{y}</option>' for y in CURRENT_YEARS)
    html = (
        CONFIGURE_HTML
        .replace("__YEAR_OPTIONS__", year_options)
        .replace("__CSP_NONCE__", request.state.csp_nonce)
    )
    return HTMLResponse(html)

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
async def health(): return {"status": "ok"}

# ── OAuth 2.0 ─────────────────────────────────────────────────────────────────

_ANILIST_AUTH_URL  = "https://anilist.co/api/v2/oauth/authorize"
_ANILIST_TOKEN_URL = "https://anilist.co/api/v2/oauth/token"


def _clear_oauth_state_cookie(response: Response) -> None:
    response.delete_cookie("oauth_state", path="/oauth")


def _oauth_error_redirect(error_code: str) -> RedirectResponse:
    response = RedirectResponse(url=f"/configure?error={error_code}")
    _clear_oauth_state_cookie(response)
    return response


class _LogoutBody(pydantic.BaseModel):
    session: str | None = None

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
    _clear_oauth_state_cookie(response)
    # Store state in a short-lived HttpOnly cookie so the callback can verify it.
    response.set_cookie(
        "oauth_state", state,
        httponly=True, samesite="lax", max_age=600, secure=_oauth_cookie_secure(), path="/oauth",
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
        return _oauth_error_redirect("auth_failed")

    # Verify state to prevent CSRF.
    if not state or not oauth_state or not secrets.compare_digest(state, oauth_state):
        logger.warning("OAuth callback state mismatch — possible CSRF attempt")
        return _oauth_error_redirect("auth_failed")

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
            error_code = "auth_failed"
            error_message = None
            try:
                error_body = resp.json()
            except Exception:
                error_body = {"raw": resp.text[:500]}
            if isinstance(error_body, dict):
                if error_body.get("error") == "invalid_client":
                    error_code = "auth_invalid_client"
                    error_message = error_body.get("message") or "client authentication failed"
                else:
                    error_message = error_body.get("message") or error_body.get("error")
            logger.error(
                "AniList token exchange failed: HTTP %d error=%s message=%s body=%r",
                resp.status_code,
                error_body.get("error") if isinstance(error_body, dict) else None,
                error_message,
                error_body,
            )
            return _oauth_error_redirect(error_code)

        access_token = resp.json().get("access_token")
        if not access_token:
            logger.error("AniList token exchange returned no access_token")
            return _oauth_error_redirect("auth_failed")

    except Exception as exc:
        logger.error("AniList token exchange error: %s", exc)
        return _oauth_error_redirect("auth_failed")

    encrypted = encrypt(access_token)
    # Store the encrypted token server-side and hand the client a short session key.
    # This keeps the full encrypted token out of the manifest URL entirely.
    # Losing the session (server restart, TTL expiry) only requires re-authentication —
    # no user data is lost.
    session_key = secrets.token_urlsafe(16)  # 22 URL-safe characters, 128 bits of entropy
    cache.set(f"session:{session_key}", encrypted, SESSION_TTL)
    # Do not log the raw access_token — only the encrypted form is safe to emit.
    logger.info("OAuth login successful; session key stored, redirecting to /configure")
    response = RedirectResponse(url=f"/configure#s={session_key}")
    _clear_oauth_state_cookie(response)
    return response


@app.post("/oauth/logout", include_in_schema=False)
async def oauth_logout(body: _LogoutBody):
    # Clear both session keys when the user explicitly disconnects.
    if body.session:
        cache.delete(f"session:{body.session}")
        cache.delete(f"session_or:{body.session}")
        cache.delete_prefix(f"ai_recs:{body.session}:")
    return {"ok": True}

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

_ALLOWED_MODELS = {
    "meta-llama/llama-3.3-70b-instruct",
    "google/gemini-flash-1.5",
    "openai/gpt-4o-mini",
    "anthropic/claude-haiku-4-5-20251001",
}
# Custom models must match org/model-name format (alphanumeric, hyphens, dots, underscores).
_MODEL_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+$")

class _SaveOrKeyBody(pydantic.BaseModel):
    session: str
    key: str | None = None   # None means "keep existing key, just update model"
    model: str = "meta-llama/llama-3.3-70b-instruct"

class _TestOrKeyBody(pydantic.BaseModel):
    key: str

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
            media = await anilist.get_favourites(raw_token, viewer["id"])
        else:
            media = await anilist.get_watching_list(raw_token, viewer["id"], body.list_status)
    except Exception as exc:
        logger.error("preview_watching failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch list from AniList.")
    return {"media": media}

@app.post("/api/save-openrouter-key")
async def api_save_openrouter_key(request: Request, body: _SaveOrKeyBody):
    """Store (or update) the user's OpenRouter API key in their session.

    The key is Fernet-encrypted before being written to the session cache —
    it is never returned in any response or written to any log.
    When *key* is None, only the model preference is updated (key unchanged).
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")

    session_key = body.session
    encrypted_anilist = cache.get(f"session:{session_key}")
    if not encrypted_anilist:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])

    model = body.model.strip() if body.model else "meta-llama/llama-3.3-70b-instruct"
    if model not in _ALLOWED_MODELS and not _MODEL_PATTERN.match(model):
        raise HTTPException(status_code=400, detail="Invalid model identifier.")
    if len(model) > 128:
        raise HTTPException(status_code=400, detail="Model identifier too long.")

    if body.key is not None:
        # New key supplied — encrypt and store.
        raw_key = body.key.strip()
        if not raw_key:
            raise HTTPException(status_code=400, detail="API key must not be empty.")
        encrypted_or = encrypt(raw_key)
        or_data = {"encrypted_key": encrypted_or, "model": model}
    else:
        # No new key — preserve existing, update model only.
        existing = cache.get(f"session_or:{session_key}")
        if not existing:
            raise HTTPException(status_code=400, detail="No OpenRouter key stored for this session. Provide a key.")
        or_data = {**existing, "model": model}

    cache.set(f"session_or:{session_key}", or_data, SESSION_TTL)
    return {"ok": True}


@app.post("/api/test-openrouter-key")
async def api_test_openrouter_key(request: Request, body: _TestOrKeyBody):
    """Make a minimal OpenRouter API call to verify the supplied key.

    Returns {"valid": true} on success. The key is used only for the test
    request and is never stored or logged.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")

    raw_key = body.key.strip()
    if not raw_key:
        raise HTTPException(status_code=400, detail="Key must not be empty.")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {raw_key}"},
            )
        if resp.status_code == 200:
            return {"valid": True}
        # 401/403 → invalid key; other errors → surface as invalid too
        return JSONResponse(status_code=400, content={"valid": False, "detail": "Key rejected by OpenRouter."})
    except Exception as exc:
        logger.error("OpenRouter key test failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not reach OpenRouter to verify the key.")


@app.post("/api/preview-ai")
async def api_preview_ai(request: Request, body: _SessionBody):
    """Return AI-recommended anime as raw AniList media dicts for the configure UI.

    Uses the same 1-hour per-session cache as the Stremio catalog route to avoid
    redundant (slow, expensive) AI calls.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")

    session_key = body.session
    raw_token = _resolve_session(session_key)

    or_data = cache.get(f"session_or:{session_key}")
    if not or_data:
        raise HTTPException(status_code=400, detail="OpenRouter API key not configured. Add it via the AI settings.")

    try:
        or_key = decrypt(or_data["encrypted_key"])
    except Exception:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])

    model = or_data.get("model", "meta-llama/llama-3.3-70b-instruct")

    # Check cache first — keyed on session + model so switching models triggers fresh recs.
    ai_cache_key = f"ai_recs:{session_key}:{model}"
    cached = cache.get(ai_cache_key)
    if cached is not None:
        return {"media": cached}

    try:
        viewer = await anilist.get_viewer(raw_token)
        raw_media = await anilist.get_ai_recommendations(raw_token, viewer["id"], or_key, model)
    except Exception as exc:
        logger.error("preview_ai failed: %s", exc)
        raise HTTPException(status_code=502, detail="AI recommendation request failed.")

    cache.set(ai_cache_key, raw_media, 60 * 60)
    return {"media": raw_media}


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
    or_data = cache.get(f"session_or:{body.session}")
    return {
        "name": viewer["name"],
        "avatar": viewer["avatar"],
        "has_or_key": or_data is not None,
        "or_model": or_data.get("model") if or_data else None,
    }

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

    encrypted_token: str | None = None
    if session_key:
        encrypted_token = cache.get(f"session:{session_key}")
    if (
        not encrypted_token
        and catalog_config.get("type") in {"watching", "ai"}
        and config.get("legacy_auth_manifest")
    ):
        raise HTTPException(
            status_code=410,
            detail="This manifest uses an old embedded AniList session. Reconnect AniList and reinstall the addon.",
        )
    try:
        metas = await _fetch_catalog(catalog_id, catalog_config, page, encrypted_token, session_key=session_key)
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

    # Resolve the AniList ID from whichever prefix was requested.
    # Meta is declared for tmdb: and anilist: only.  tt* items get rich meta
    # from Cinemeta.  We still accept tt* here for direct URL access.
    if item_id.startswith("anilist:"):
        raw_id = item_id.removeprefix("anilist:")
        if not raw_id.isdigit():
            raise HTTPException(status_code=400, detail="Invalid AniList ID")
        anilist_id = int(raw_id)
    elif item_id.startswith("tmdb:"):
        raw_id = item_id.removeprefix("tmdb:")
        if not raw_id.isdigit():
            raise HTTPException(status_code=400, detail="Invalid TMDB ID")
        anilist_id = await reverse_lookup(item_id)
        if not anilist_id:
            raise HTTPException(status_code=404, detail="Could not resolve TMDB ID to AniList")
    elif item_id.startswith("tt"):
        if not item_id[2:].isdigit():
            raise HTTPException(status_code=400, detail="Invalid IMDB ID")
        anilist_id = await reverse_lookup(item_id)
        if not anilist_id:
            raise HTTPException(status_code=404, detail="Could not resolve IMDB ID to AniList")
    else:
        raise HTTPException(status_code=404, detail="Unknown ID prefix")

    cache_key = f"meta:{anilist_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        # Return with the originally requested ID for Fusion consistency.
        return JSONResponse({"meta": {**cached, "id": item_id}})
    try:
        meta_data = await anilist.get_meta(anilist_id)
    except Exception as exc:
        logger.error("Meta fetch failed for %d: %s", anilist_id, exc)
        raise HTTPException(status_code=502, detail="AniList API error") from exc
    if not meta_data:
        raise HTTPException(status_code=404, detail="Anime not found")
    cache.set(cache_key, meta_data, TTL["meta"])
    # Override the id field with the originally requested ID.
    return JSONResponse({"meta": {**meta_data, "id": item_id}})

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
