"""
Config encoding/decoding.

User preferences are stored as base64-encoded JSON in the manifest URL:
    http://host:7000/eyJjYXRhbG9ncyI6...}/manifest.json

This means zero database, zero state on the server. The config travels
with the URL the user installs in Stremio/Fusion.

Config shape:
{
    "catalogs": [
        {
            "id": "anilist-popular-season",   # built-in preset ID
            "name": "Popular This Season",    # display name (user can rename)
            "type": "preset"                  # "preset" | "custom" | "watching"
        },
        {
            "id": "custom-abc123",            # generated for custom catalogs
            "name": "My Action Picks",
            "type": "custom",
            "filters": {
                "genres": ["Action", "Adventure"],
                "year": 2024,
                "season": "FALL",
                "format": "TV",
                "status": "RELEASING",
                "sort": "POPULARITY_DESC",
                "minScore": 70
            }
        },
        {
            "id": "anilist-watching",         # authenticated user's watch list
            "name": "My Watching List",
            "type": "watching"
        }
    ],
    # Note: no "token" field — auth is handled via a short server-side auth key
    # appended to the manifest URL path as "{config_token}~{session_key}".
}

Compact wire format (gzip-compressed, then base64url-encoded):
    {"c": [{...catalog entries...}]}

The AniList token is NOT stored in this payload. It lives server-side in a
durable encrypted auth store, keyed by a randomly-generated auth key that is
appended to the URL path segment with a "~" separator:
    http://host:7000/{config_token}~{session_key}/manifest.json

Losing the auth key only happens if the user disconnects or the server's
durable auth database is lost — catalog configuration still lives in the URL.
"""

import base64
import gzip
import json
import hashlib
from typing import Any

PRESET_NAMES = {
    "anilist-popular-season": "Popular This Season",
    "anilist-airing-week":    "Airing This Week",
    "anilist-trending":       "Trending Now",
    "anilist-top-rated":      "Top Rated All Time",
}

POSTER_STYLE_DEFAULT = "clean"
POSTER_STYLES = {"clean", "rank", "rating", "cinematic", "anilist"}


def _normalize_poster_style(value: Any) -> str:
    style = str(value or POSTER_STYLE_DEFAULT).strip().lower()
    return style if style in POSTER_STYLES else POSTER_STYLE_DEFAULT

DEFAULT_CONFIG = {
    "catalogs": [
        {"id": "anilist-popular-season", "name": "Popular This Season", "type": "preset"},
        {"id": "anilist-airing-week",    "name": "Airing This Week",    "type": "preset"},
        {"id": "anilist-trending",       "name": "Trending Now",        "type": "preset"},
        {"id": "anilist-top-rated",      "name": "Top Rated All Time",  "type": "preset"},
    ]
}


def _compact_media_ref(ref: Any) -> dict[str, Any] | None:
    if not isinstance(ref, dict):
        return None
    try:
        media_id = int(ref.get("id") or 0)
    except (TypeError, ValueError):
        media_id = 0
    title = str(ref.get("title") or "").strip()
    if media_id <= 0 and not title:
        return None
    entry: dict[str, Any] = {}
    if media_id > 0:
        entry["i"] = media_id
    if title:
        entry["t"] = title[:160]
    return entry or None


def _expand_media_ref(entry: Any) -> dict[str, Any] | None:
    if not isinstance(entry, dict):
        return None
    ref: dict[str, Any] = {}
    try:
        media_id = int(entry.get("i") or 0)
    except (TypeError, ValueError):
        media_id = 0
    if media_id > 0:
        ref["id"] = media_id
    title = str(entry.get("t") or "").strip()
    if title:
        ref["title"] = title[:160]
    return ref or None


def _compact_catalog_entry(cat: Any) -> dict[str, Any]:
    if not isinstance(cat, dict):
        return {"i": "", "n": "", "f": {}}

    cat_id = cat.get("id", "")
    if cat_id in PRESET_NAMES:
        entry: dict[str, Any] = {"i": cat_id}
        default_name = PRESET_NAMES[cat_id]
        if cat.get("name") and cat["name"] != default_name:
            entry["n"] = cat["name"]
        if cat.get("randomize"):
            entry["r"] = True
        return entry

    if cat.get("type") == "watching":
        entry = {"i": cat_id, "n": cat.get("name", cat_id), "w": True}
        if cat.get("listStatus"):
            entry["s"] = cat["listStatus"]
        if cat.get("clientFilters"):
            entry["cf"] = cat["clientFilters"]
        if cat.get("sourceName"):
            entry["sn"] = str(cat["sourceName"])[:120]
        if cat.get("randomize"):
            entry["r"] = True
        return entry

    if cat.get("type") == "ai":
        entry = {"i": cat_id, "n": cat.get("name", cat_id), "a": True}
        default_model = "meta-llama/llama-3.3-70b-instruct"
        if cat.get("model") and cat["model"] != default_model:
            entry["m"] = cat["model"]
        if cat.get("aiMode"):
            entry["am"] = cat["aiMode"]
        if cat.get("seedMediaId"):
            entry["sid"] = cat["seedMediaId"]
        if cat.get("seedTitle"):
            entry["st"] = cat["seedTitle"]
        if cat.get("smartOptions"):
            entry["so"] = cat["smartOptions"]
        if cat.get("clientFilters"):
            entry["cf"] = cat["clientFilters"]
        if cat.get("sourceName"):
            entry["sn"] = str(cat["sourceName"])[:120]
        if cat.get("randomize"):
            entry["r"] = True
        return entry

    entry = {"i": cat_id, "n": cat.get("name", cat_id), "f": cat.get("filters", {})}
    if cat.get("clientFilters"):
        entry["cf"] = cat["clientFilters"]
    if isinstance(cat.get("baseCatalog"), dict):
        entry["bc"] = _compact_catalog_entry(cat["baseCatalog"])
    included = [
        compacted
        for compacted in (_compact_media_ref(ref) for ref in (cat.get("includedMedia") or []))
        if compacted
    ]
    if included:
        entry["im"] = included
    seed = _compact_media_ref(cat.get("searchSeed"))
    if seed:
        entry["ss"] = seed
    if cat.get("randomize"):
        entry["r"] = True
    return entry


def _expand_catalog_entry(entry: Any) -> dict[str, Any]:
    if not isinstance(entry, dict):
        return {"id": "", "name": "", "type": "custom", "filters": {}}

    cat_id = entry.get("i", "")
    if cat_id in PRESET_NAMES:
        cat: dict[str, Any] = {
            "id": cat_id,
            "name": entry.get("n", PRESET_NAMES[cat_id]),
            "type": "preset",
        }
    elif entry.get("w"):
        cat = {
            "id": cat_id,
            "name": entry.get("n", cat_id),
            "type": "watching",
        }
        if entry.get("s"):
            cat["listStatus"] = entry["s"]
        if entry.get("cf"):
            cat["clientFilters"] = entry["cf"]
        if entry.get("sn"):
            cat["sourceName"] = entry["sn"]
    elif entry.get("a"):
        cat = {
            "id": cat_id,
            "name": entry.get("n", cat_id),
            "type": "ai",
            "model": entry.get("m", "meta-llama/llama-3.3-70b-instruct"),
        }
        if entry.get("am"):
            cat["aiMode"] = entry["am"]
        if entry.get("sid"):
            cat["seedMediaId"] = entry["sid"]
        if entry.get("st"):
            cat["seedTitle"] = entry["st"]
        if entry.get("so"):
            cat["smartOptions"] = entry["so"]
        if entry.get("cf"):
            cat["clientFilters"] = entry["cf"]
        if entry.get("sn"):
            cat["sourceName"] = entry["sn"]
    else:
        cat = {
            "id": cat_id,
            "name": entry.get("n", cat_id),
            "type": "custom",
            "filters": entry.get("f", {}),
        }
        if entry.get("cf"):
            cat["clientFilters"] = entry["cf"]
        if isinstance(entry.get("bc"), dict):
            cat["baseCatalog"] = _expand_catalog_entry(entry["bc"])
        included = [
            expanded
            for expanded in (_expand_media_ref(ref) for ref in (entry.get("im") or []))
            if expanded
        ]
        if included:
            cat["includedMedia"] = included
        seed = _expand_media_ref(entry.get("ss"))
        if seed:
            cat["searchSeed"] = seed

    if entry.get("r"):
        cat["randomize"] = True
    return cat


def encode_config(config: dict) -> str:
    """Encode a config dict to a compact gzip+base64url string.

    Compact format: {"c": [{i, n?, r?}, ...]}
    Preset catalogs: only {i} (name omitted if default, randomize omitted if false).
    Custom catalogs: {i, n, f} plus optional r.

    The AniList token is NOT embedded here — it is handled via a short server-side
    auth key appended to the URL segment as "{config_token}~{session_key}".
    """
    compact = [_compact_catalog_entry(cat) for cat in config.get("catalogs", [])]
    payload: dict[str, Any] = {"c": compact}
    poster_style = _normalize_poster_style(config.get("posterStyle") or config.get("poster_style"))
    if poster_style != POSTER_STYLE_DEFAULT:
        payload["ps"] = poster_style
    json_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    compressed = gzip.compress(json_bytes, compresslevel=9, mtime=0)
    return base64.urlsafe_b64encode(compressed).decode("utf-8").rstrip("=")


def decode_config(token: str) -> dict:
    """Decode a config token back to a dict. Returns default config on failure.

    Handles:
    - Gzip-compressed payloads (magic bytes 0x1f 0x8b) — new format
    - Uncompressed base64url payloads — legacy format
    - Both compact {"c": [...]} and verbose {"catalogs": [...]} JSON shapes
    """
    try:
        padding = 4 - len(token) % 4
        if padding != 4:
            token += "=" * padding
        raw = base64.urlsafe_b64decode(token)
        if raw[:2] == b"\x1f\x8b":
            json_bytes = gzip.decompress(raw)
        else:
            json_bytes = raw
        payload = json.loads(json_bytes.decode("utf-8"))
        if not isinstance(payload, dict):
            return DEFAULT_CONFIG
        # Compact format
        if "c" in payload:
            catalogs = [_expand_catalog_entry(entry) for entry in payload["c"]]
            result: dict[str, Any] = {"catalogs": catalogs}
            if payload.get("ps"):
                result["posterStyle"] = _normalize_poster_style(payload.get("ps"))
            if payload.get("t"):
                result["legacy_auth_manifest"] = True
            return result
        # Legacy verbose format
        if "catalogs" not in payload:
            return DEFAULT_CONFIG
        if payload.get("token"):
            payload = {**payload, "legacy_auth_manifest": True}
        if payload.get("posterStyle") or payload.get("poster_style"):
            payload["posterStyle"] = _normalize_poster_style(payload.get("posterStyle") or payload.get("poster_style"))
        return payload
    except Exception:
        return DEFAULT_CONFIG


def make_custom_id(filters: dict) -> str:
    """Generate a stable short ID for a custom catalog based on its filters."""
    stable = json.dumps(filters, sort_keys=True, separators=(",", ":"))
    return "custom-" + hashlib.md5(stable.encode()).hexdigest()[:8]


DEFAULT_CONFIG_TOKEN = encode_config(DEFAULT_CONFIG)


# ---------------------------------------------------------------------------
# Filter option definitions (used by both the UI and the query builder)
# ---------------------------------------------------------------------------

GENRES = [
    "Action", "Adventure", "Comedy", "Drama", "Ecchi", "Fantasy",
    "Horror", "Mahou Shoujo", "Mecha", "Music", "Mystery", "Psychological",
    "Romance", "Sci-Fi", "Slice of Life", "Sports", "Supernatural", "Thriller"
]

SEASONS = ["WINTER", "SPRING", "SUMMER", "FALL"]

FORMATS = ["TV", "TV_SHORT", "MOVIE", "OVA", "ONA", "SPECIAL"]

STATUSES = ["RELEASING", "FINISHED", "NOT_YET_RELEASED", "CANCELLED"]

SORT_OPTIONS = {
    "POPULARITY_DESC": "Most Popular",
    "TRENDING_DESC":   "Trending",
    "SCORE_DESC":      "Highest Rated",
    "START_DATE_DESC": "Newest",
    "FAVOURITES_DESC": "Most Favourited",
}

from datetime import datetime as _dt
CURRENT_YEARS = list(range(_dt.now().year + 1, 1979, -1))
