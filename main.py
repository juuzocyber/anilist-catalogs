"""
AniList Catalogs — FastAPI entry point.
"""

import asyncio
import hashlib
import io
import json
import logging
import math
import os
import random
import re
import secrets
import time
from contextlib import asynccontextmanager, suppress
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse

import httpx
import pydantic

from fastapi import FastAPI, HTTPException, Request, Cookie, Response
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, FileResponse

import anilist
import id_mapper
from auth_store import auth_store
from cache import cache, TTL
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
    AUTH_DB_PATH,
    ENABLE_API_DOCS,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)
PER_PAGE = 50
_SHARED_HTTP_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)
_ANILIST_HTTP_CLIENT_TIMEOUT = httpx.Timeout(10.0)
_GENERAL_HTTP_CLIENT_TIMEOUT = httpx.Timeout(30.0)
_FRIBB_WARMUP_TIMEOUT = 8.0
_RANDOMIZE_BUCKET_SECONDS = 6 * 60 * 60
_API_MAX_CONTENT_LENGTH = 32_768
_MAX_SESSION_KEY_LENGTH = 128
_MAX_OPENROUTER_KEY_LENGTH = 512
_MAX_AI_CATALOG_CONFIG_BYTES = 8_192
_SESSION_KEY_PATTERN = re.compile(r"^[A-Za-z0-9._~-]+$")
_STATIC_DIR = Path(__file__).resolve().parent / "static"
_STATIC_ASSETS = {
    "qrcode.min.js": ("qrcode.min.js", "application/javascript; charset=utf-8"),
    "MonaSansVF.woff2": ("MonaSansVF.woff2", "font/woff2"),
}
_anilist_http_client: httpx.AsyncClient | None = None
_general_http_client: httpx.AsyncClient | None = None

PRESET_HANDLERS = {
    "anilist-popular-season": anilist.get_popular_season,
    "anilist-airing-week":    anilist.get_airing_week,
    "anilist-trending":       anilist.get_trending,
    "anilist-top-rated":      anilist.get_top_rated,
}
POSTER_LAB_VARIANT = "poster-lab"
POSTER_LAB_VERSION = "v9"
POSTER_LAB_DEFAULT_STYLE = "clean"
POSTER_LAB_STYLES = {"clean", "rank", "rating"}
_POSTER_LAB_ALLOWED_HOST_SUFFIXES = ("anilist.co", "anili.st")
_CATALOG_CACHE_VERSION = "v3"
_POSTER_LAB_SEASONAL_STATUSES = {"RELEASING", "NOT_YET_RELEASED"}
_POSTER_LAB_RETURNING_RELATIONS = {"PREQUEL"}
_POSTER_LAB_SPINOFF_RELATIONS = {"PARENT"}
_POSTER_LAB_SOURCE_LABELS = {
    "MANGA": "Manga Adaptation",
    "LIGHT_NOVEL": "LN Adaptation",
    "VIDEO_GAME": "Game Adaptation",
}
_POSTER_LAB_ORIGINAL_SOURCE = "ORIGINAL"
_POSTER_LAB_ANIME_SOURCE = "ANIME"
_POSTER_LAB_MOVIE_PREMIERE_DAYS = 45
_POSTER_LAB_RECENT_ADAPTATION_DAYS = 90
_POSTER_LAB_AIRS_THIS_WEEK_SECONDS = 7 * 24 * 60 * 60
_POSTER_LAB_TRENDING_TOP_N = 10
_POSTER_LAB_TOP_RANK_PRIORITY_LIMIT = 100
_POSTER_LAB_TOP_BANNER_REFERENCE_LABEL = "Manga Adaptation"
_MAPPING_EXAMPLE_LIMIT = 5
SMART_AI_MODES = {"title_seed", "top_rated", "hidden_completed"}
SMART_AI_FORMATS = {"TV", "TV_SHORT", "MOVIE", "OVA", "ONA", "SPECIAL"}
SMART_AI_POPULARITY_BIASES = {"balanced", "hidden", "mainstream"}
SEARCH_RESULT_LIMIT = 8
_MAX_CATALOG_NESTING = 5

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

def _build_manifest(config, *, poster_variant: str = "default"):
    catalogs = []
    for cat in config.get("catalogs", []):
        catalogs.append({"type": "series", "id": cat["id"], "name": cat["name"], "extra": [{"name": "skip", "isRequired": False}]})
    m = dict(MANIFEST)
    if poster_variant == POSTER_LAB_VARIANT:
        m["id"] = f"{MANIFEST['id']}.posterlab"
        m["name"] = f"{MANIFEST['name']} Poster Styles"
        m["description"] = (
            "AniList Catalogs variant with combined, rank-only, and rating-only poster overlays."
        )
    m["catalogs"] = catalogs
    m["behaviorHints"] = {**m.get("behaviorHints", {}), "configurable": True, "configurationRequired": False}
    return m


def _poster_lab_base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


def _poster_lab_normalize_style(style: str | None) -> str:
    normalized = (style or POSTER_LAB_DEFAULT_STYLE).strip().lower()
    return normalized if normalized in POSTER_LAB_STYLES else POSTER_LAB_DEFAULT_STYLE


def _poster_lab_season_for_datetime(now: datetime) -> tuple[str, int]:
    month = now.month
    if month in (1, 2, 3):
        return "WINTER", now.year
    if month in (4, 5, 6):
        return "SPRING", now.year
    if month in (7, 8, 9):
        return "SUMMER", now.year
    return "FALL", now.year


def _poster_lab_start_date(media: dict) -> date | None:
    start = media.get("startDate") or {}
    year = start.get("year")
    month = start.get("month")
    day = start.get("day")
    if not all(isinstance(part, int) and part > 0 for part in (year, month, day)):
        return None
    try:
        return date(year, month, day)
    except ValueError:
        return None


def _poster_lab_relation_types(media: dict) -> set[str]:
    relation_types: set[str] = set()
    edges = ((media.get("relations") or {}).get("edges")) or []
    for edge in edges:
        if not isinstance(edge, dict):
            continue
        node = edge.get("node") or {}
        if str(node.get("type") or "").upper() != "ANIME":
            continue
        relation_type = str(edge.get("relationType") or "").upper()
        if relation_type:
            relation_types.add(relation_type)
    return relation_types


def _poster_lab_rank_info(media: dict) -> tuple[int | None, str | None]:
    rankings = media.get("rankings") or []
    popular_all_time = next(
        (
            ranking for ranking in rankings
            if (ranking.get("type") or "").upper() == "POPULAR"
            and ranking.get("allTime") is True
            and isinstance(ranking.get("rank"), int)
            and ranking.get("rank") <= 200
        ),
        None,
    )
    score_all_time = next(
        (
            ranking for ranking in rankings
            if (ranking.get("type") or "").upper() == "RATED"
            and ranking.get("allTime") is True
            and isinstance(ranking.get("rank"), int)
            and ranking.get("rank") <= 200
        ),
        None,
    )
    candidates: list[tuple[int, str]] = []
    if popular_all_time:
        candidates.append((popular_all_time["rank"], "Most Popular"))
    if score_all_time:
        candidates.append((score_all_time["rank"], "Highest Rated"))
    if candidates:
        best_rank, label = min(candidates, key=lambda item: item[0])
        return best_rank, f"#{best_rank} {label}"
    return None, None


def _poster_lab_rank_fallback_label(media: dict) -> str | None:
    return _poster_lab_rank_info(media)[1]


def _poster_lab_trending_ids(media_items: list[dict]) -> set[int]:
    ranked: list[tuple[int, int, int]] = []
    for index, media in enumerate(media_items):
        media_id = media.get("id")
        trending = media.get("trending")
        if not isinstance(media_id, int) or not isinstance(trending, int) or trending <= 0:
            continue
        ranked.append((trending, -index, media_id))
    ranked.sort(reverse=True)
    return {media_id for _, _, media_id in ranked[:_POSTER_LAB_TRENDING_TOP_N]}


def _poster_lab_top_label(
    media: dict,
    media_items: list[dict] | None = None,
    *,
    now: datetime | None = None,
    trending_ids: set[int] | None = None,
) -> str | None:
    now_utc = now or datetime.now(timezone.utc)
    today = now_utc.date()
    current_season, current_year = _poster_lab_season_for_datetime(now_utc)
    season = str(media.get("season") or "").upper()
    season_year = media.get("seasonYear")
    status = str(media.get("status") or "").upper()
    media_format = str(media.get("format") or "").upper()
    source = str(media.get("source") or "").upper()
    relation_types = _poster_lab_relation_types(media)
    start_date = _poster_lab_start_date(media)
    best_rank, rank_label = _poster_lab_rank_info(media)
    if best_rank is not None and best_rank <= _POSTER_LAB_TOP_RANK_PRIORITY_LIMIT:
        return rank_label

    is_current_season_release = (
        season == current_season
        and season_year == current_year
        and status in _POSTER_LAB_SEASONAL_STATUSES
    )
    if is_current_season_release and relation_types.intersection(_POSTER_LAB_RETURNING_RELATIONS):
        return "Returning Series"
    if relation_types.intersection(_POSTER_LAB_SPINOFF_RELATIONS):
        return "Spin-off"
    if is_current_season_release:
        return "New Season"
    if media_format == "MOVIE" and start_date and abs((start_date - today).days) <= _POSTER_LAB_MOVIE_PREMIERE_DAYS:
        return "Movie Premiere"
    if source in _POSTER_LAB_SOURCE_LABELS:
        return _POSTER_LAB_SOURCE_LABELS[source]
    if (
        source
        and source not in {_POSTER_LAB_ORIGINAL_SOURCE, _POSTER_LAB_ANIME_SOURCE}
        and start_date
        and 0 <= (today - start_date).days <= _POSTER_LAB_RECENT_ADAPTATION_DAYS
    ):
        return "Recently Adapted"
    if source == _POSTER_LAB_ORIGINAL_SOURCE:
        return "Original Anime"

    next_airing = media.get("nextAiringEpisode") or {}
    time_until_airing = next_airing.get("timeUntilAiring")
    if (
        status == "RELEASING"
        and isinstance(time_until_airing, int)
        and 0 <= time_until_airing <= _POSTER_LAB_AIRS_THIS_WEEK_SECONDS
    ):
        return "Airs This Week"

    effective_trending_ids = trending_ids
    if effective_trending_ids is None and media_items is not None:
        effective_trending_ids = _poster_lab_trending_ids(media_items)
    if isinstance(media.get("id"), int) and effective_trending_ids and media["id"] in effective_trending_ids:
        return "Trending Now"

    return rank_label


def _poster_lab_top_labels(media_items: list[dict], *, now: datetime | None = None) -> dict[int, str]:
    effective_now = now or datetime.now(timezone.utc)
    trending_ids = _poster_lab_trending_ids(media_items)
    labels: dict[int, str] = {}
    for media in media_items:
        media_id = media.get("id")
        if not isinstance(media_id, int):
            continue
        label = _poster_lab_top_label(media, media_items, now=effective_now, trending_ids=trending_ids)
        if label:
            labels[media_id] = label
    return labels


def _poster_lab_bottom_label(media: dict) -> str | None:
    first_genre = next((genre for genre in (media.get("genres") or []) if genre), None)
    score = media.get("averageScore") or media.get("meanScore")
    rating = f"{score / 10:.1f}" if score else None
    if first_genre and rating:
        return f"{first_genre}|{rating}"
    return first_genre or rating


def _poster_lab_badge_color(media: dict) -> str | None:
    cover = media.get("coverImage") or {}
    color = cover.get("color")
    if not isinstance(color, str):
        return None
    color = color.strip()
    if re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        return color.lower()
    return None


def _poster_lab_poster_url(
    base_url: str,
    media: dict,
    *,
    style: str = POSTER_LAB_DEFAULT_STYLE,
    top_label: str | None = None,
) -> str | None:
    cover = media.get("coverImage") or {}
    source_url = cover.get("extraLarge") or cover.get("large")
    if not source_url:
        return None
    poster_style = _poster_lab_normalize_style(style)
    params = {
        "src": source_url,
        "top": ((top_label if top_label is not None else _poster_lab_top_label(media)) or "")[:64],
        "bottom": (_poster_lab_bottom_label(media) or "")[:36],
        "badge": _poster_lab_badge_color(media) or "",
        "style": poster_style,
        "v": POSTER_LAB_VERSION,
    }
    return f"{base_url}/poster-lab/render.png?{urlencode(params)}"


def _poster_lab_cache_key(
    catalog_id: str,
    page: int,
    *,
    cache_scope: str = "",
    poster_variant: str = "default",
    poster_base_url: str | None = None,
    poster_style: str = POSTER_LAB_DEFAULT_STYLE,
) -> str:
    scope_hash = hashlib.sha1(cache_scope.encode("utf-8")).hexdigest()[:10] if cache_scope else "default"
    if poster_variant == "default":
        return f"catalog:{catalog_id}:page:{page}:scope:{scope_hash}:cache:{_CATALOG_CACHE_VERSION}"
    base_hash = hashlib.sha1((poster_base_url or "").encode("utf-8")).hexdigest()[:8]
    style = _poster_lab_normalize_style(poster_style)
    return (
        f"catalog:{catalog_id}:page:{page}:scope:{scope_hash}:cache:{_CATALOG_CACHE_VERSION}:"
        f"variant:{poster_variant}:{style}:{POSTER_LAB_VERSION}:{base_hash}"
    )


def _poster_lab_allow_source(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return False
    hostname = parsed.hostname.lower()
    return any(hostname == suffix or hostname.endswith(f".{suffix}") for suffix in _POSTER_LAB_ALLOWED_HOST_SUFFIXES)


def _poster_lab_effect_profile(style: str | None) -> dict[str, int | float]:
    normalized_style = _poster_lab_normalize_style(style)
    if normalized_style in {"clean", "rating"}:
        return {
            "blur_ratio": 0.34,
            "blur_alpha": 236,
            "blur_min_radius": 10,
            "blur_width_divisor": 46,
            "shadow_ratio": 0.24,
            "shadow_alpha": 132,
        }
    return {
        "blur_ratio": 0.26,
        "blur_alpha": 220,
        "blur_min_radius": 8,
        "blur_width_divisor": 58,
        "shadow_ratio": 0.20,
        "shadow_alpha": 105,
    }


def _poster_lab_font_candidates(bold: bool) -> list[str]:
    if bold:
        return [
            "C:\\Windows\\Fonts\\segoeuib.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        ]
    return [
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]


def _poster_lab_load_font(size: int, *, bold: bool = False):
    from PIL import ImageFont

    for path in _poster_lab_font_candidates(bold):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def _poster_lab_fit_font(text: str, max_width: int, max_size: int, min_size: int, *, bold: bool):
    from PIL import Image, ImageDraw

    probe = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    for size in range(max_size, min_size - 1, -2):
        font = _poster_lab_load_font(size, bold=bold)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        width = right - left
        if width <= max_width:
            return font
    return _poster_lab_load_font(min_size, bold=bold)


def _poster_lab_fit_font_with_size(text: str, max_width: int, max_size: int, min_size: int, *, bold: bool):
    from PIL import Image, ImageDraw

    probe = Image.new("RGBA", (8, 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    for size in range(max_size, min_size - 1, -2):
        font = _poster_lab_load_font(size, bold=bold)
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
        width = right - left
        if width <= max_width:
            return font, size
    return _poster_lab_load_font(min_size, bold=bold), min_size


def _poster_lab_text_size(draw, text: str, font) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def _poster_lab_top_banner_metrics(draw, target_width: int, target_height: int, top_text: str):
    max_size = int(target_width * 0.075)
    reference_font, reference_size = _poster_lab_fit_font_with_size(
        _POSTER_LAB_TOP_BANNER_REFERENCE_LABEL,
        int(target_width * 0.82),
        max_size,
        24,
        bold=True,
    )
    reference_width, reference_height = _poster_lab_text_size(draw, _POSTER_LAB_TOP_BANNER_REFERENCE_LABEL, reference_font)
    chip_padding_x = int(target_width * 0.048)
    chip_padding_y = int(target_height * 0.019)
    chip_width = target_width
    max_text_width = chip_width - (chip_padding_x * 2)
    font = _poster_lab_fit_font(top_text, max_text_width, reference_size, max(20, reference_size - 6), bold=True)
    text_width, text_height = _poster_lab_text_size(draw, top_text, font)
    chip_height = reference_height + (chip_padding_y * 2)
    return {
        "font": font,
        "text_width": text_width,
        "text_height": text_height,
        "chip_width": chip_width,
        "chip_height": chip_height,
    }


def _poster_lab_draw_star(draw, center: tuple[float, float], outer_radius: float, *, fill: tuple[int, int, int, int]) -> None:
    points: list[tuple[float, float]] = []
    inner_radius = outer_radius * 0.48
    for index in range(10):
        angle = math.radians(-90 + (index * 36))
        radius = outer_radius if index % 2 == 0 else inner_radius
        points.append((
            center[0] + math.cos(angle) * radius,
            center[1] + math.sin(angle) * radius,
        ))
    draw.polygon(points, fill=fill)


def _poster_lab_draw_bottom_rounded_badge(draw, box: tuple[int, int, int, int], radius: int, *, fill: tuple[int, int, int, int]) -> None:
    left, top, right, bottom = box
    radius = max(0, min(radius, (right - left) // 2, (bottom - top) // 2))
    if radius == 0:
        draw.rectangle(box, fill=fill)
        return
    draw.rectangle((left, top, right, bottom - radius), fill=fill)
    draw.rectangle((left + radius, bottom - radius, right - radius, bottom), fill=fill)
    draw.pieslice((left, bottom - (radius * 2), left + (radius * 2), bottom), 90, 180, fill=fill)
    draw.pieslice((right - (radius * 2), bottom - (radius * 2), right, bottom), 0, 90, fill=fill)


def _poster_lab_badge_fill(badge_color: str | None) -> tuple[int, int, int, int]:
    if not badge_color or not re.fullmatch(r"#[0-9a-fA-F]{6}", badge_color):
        return (30, 31, 34, 238)
    red = int(badge_color[1:3], 16)
    green = int(badge_color[3:5], 16)
    blue = int(badge_color[5:7], 16)
    # Pull the poster theme darker so the white badge text stays readable.
    red = max(16, min(255, int(red * 0.42)))
    green = max(16, min(255, int(green * 0.42)))
    blue = max(16, min(255, int(blue * 0.42)))
    return (red, green, blue, 238)


async def _render_poster_lab_image(
    source_url: str,
    top_label: str,
    bottom_label: str,
    badge_color: str | None = None,
    *,
    style: str = POSTER_LAB_DEFAULT_STYLE,
) -> bytes:
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError as exc:
        raise HTTPException(status_code=500, detail="Poster banners require Pillow. Install the updated requirements first.") from exc

    if not _poster_lab_allow_source(source_url):
        raise HTTPException(status_code=400, detail="Unsupported poster source host.")

    try:
        response = await _request_with_general_client("GET", source_url, timeout=20.0)
        response.raise_for_status()
    except Exception as exc:
        logger.error("Poster banners could not fetch source poster %s: %s", source_url, exc)
        raise HTTPException(status_code=502, detail="Could not fetch source poster.") from exc

    try:
        base = Image.open(io.BytesIO(response.content)).convert("RGBA")
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Source poster was not a supported image.") from exc

    # Keep AniList's original poster dimensions so the experimental path uses
    # the same underlying image quality as the normal preview instead of
    # downscaling and re-sampling before we draw the overlays.
    poster = base.copy().convert("RGBA")
    target_width, target_height = poster.size

    poster_style = _poster_lab_normalize_style(style)
    effect_profile = _poster_lab_effect_profile(poster_style)

    if poster_style in {"clean", "rank", "rating"}:
        blur_height = int(target_height * effect_profile["blur_ratio"])
        blur_top = max(0, target_height - blur_height)
        blurred_poster = poster.filter(
            ImageFilter.GaussianBlur(
                radius=max(effect_profile["blur_min_radius"], target_width // effect_profile["blur_width_divisor"])
            )
        )
        blur_mask = Image.new("L", poster.size, 0)
        mask_draw = ImageDraw.Draw(blur_mask)
        for offset in range(blur_height):
            alpha = int(effect_profile["blur_alpha"] * ((offset + 1) / max(blur_height, 1)))
            y0 = blur_top + offset
            mask_draw.rectangle((0, y0, target_width, y0 + 1), fill=alpha)
        poster = Image.composite(blurred_poster, poster, blur_mask)

    shadow = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_height = int(target_height * effect_profile["shadow_ratio"])
    shadow_alpha = effect_profile["shadow_alpha"]
    for offset in range(shadow_height):
        alpha = int(shadow_alpha * (1 - (offset / max(shadow_height, 1))))
        y0 = target_height - offset - 1
        shadow_draw.rectangle((0, y0, target_width, y0 + 1), fill=(0, 0, 0, alpha))
    poster = Image.alpha_composite(poster, shadow)

    draw = ImageDraw.Draw(poster, "RGBA")
    margin = int(target_width * 0.045)
    top_text = (top_label or "").strip()
    bottom_text = (bottom_label or "").strip()
    top_fill = _poster_lab_badge_fill(badge_color)
    genre_text, rating_text = (bottom_text.split("|", 1) + [""])[:2]
    genre_text = genre_text.strip()
    rating_text = rating_text.strip()

    if top_text and poster_style in {"clean", "rank"}:
        banner_metrics = _poster_lab_top_banner_metrics(draw, target_width, target_height, top_text)
        font = banner_metrics["font"]
        chip_width = min(target_width, banner_metrics["chip_width"])
        chip_height = banner_metrics["chip_height"]
        top_box = (
            0,
            0,
            chip_width,
            chip_height + int(target_height * 0.004),
        )
        radius = max(6, int(chip_height * 0.22))
        _poster_lab_draw_bottom_rounded_badge(draw, top_box, radius, fill=top_fill)
        draw.text(
            ((top_box[0] + top_box[2]) / 2, (top_box[1] + top_box[3]) / 2),
            top_text,
            fill=(255, 255, 255, 252),
            font=font,
            anchor="mm",
        )

    if bottom_text and poster_style in {"clean", "rating"}:
        font = _poster_lab_fit_font(
            f"{genre_text} {rating_text}".strip(),
            int(target_width * (0.88 if poster_style == "rating" else 0.82)),
            int(target_width * (0.090 if poster_style == "rating" else 0.082)),
            28,
            bold=True,
        )
        genre_width, text_height = _poster_lab_text_size(draw, genre_text or rating_text, font)
        rating_width = _poster_lab_text_size(draw, rating_text, font)[0] if rating_text else 0
        gap = int(target_width * 0.02)
        dot_size = max(8, target_width // 62)
        star_size = max(12, target_width // 30)
        content_width = genre_width
        if rating_text:
            if genre_text:
                content_width += gap + dot_size + gap
            content_width += star_size + gap + rating_width
        cursor_x = (target_width - content_width) / 2
        center_y = target_height - margin - max(text_height, star_size) * 1.93
        if genre_text:
            draw.text((cursor_x, center_y), genre_text, fill=(174, 176, 180, 255), font=font, anchor="lm")
            cursor_x += genre_width
        if rating_text and genre_text:
            cursor_x += gap
            dot_y = int(center_y + max(1, text_height * 0.08))
            draw.ellipse((cursor_x, dot_y - dot_size // 2, cursor_x + dot_size, dot_y + dot_size // 2), fill=(171, 173, 177, 245))
            cursor_x += dot_size + gap
        if rating_text:
            larger_star_size = max(star_size * 1.82, text_height * 1.12)
            star_center_y = center_y + max(1, text_height * 0.08)
            _poster_lab_draw_star(draw, (cursor_x + (larger_star_size / 2), star_center_y), larger_star_size / 2, fill=(196, 186, 182, 255))
            cursor_x += larger_star_size + gap
            draw.text((cursor_x, center_y), rating_text, fill=(196, 186, 182, 255), font=font, anchor="lm")

    output = io.BytesIO()
    poster.convert("RGB").save(output, format="PNG", optimize=True)
    return output.getvalue()


def _current_randomize_bucket(now: float | None = None) -> int:
    timestamp = time.time() if now is None else now
    return int(timestamp // _RANDOMIZE_BUCKET_SECONDS)


def _stable_shuffle_metas(
    metas: list[dict],
    *,
    config_token: str,
    catalog_id: str,
    page: int,
    bucket: int | None = None,
) -> list[dict]:
    if len(metas) < 2:
        return list(metas)

    if bucket is None:
        bucket = _current_randomize_bucket()

    seed_material = f"{config_token}:{catalog_id}:{page}:{bucket}".encode("utf-8")
    seed = int.from_bytes(hashlib.sha256(seed_material).digest()[:8], "big")
    shuffled = list(metas)
    random.Random(seed).shuffle(shuffled)
    return shuffled


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


def _build_shared_http_client(*, timeout: httpx.Timeout) -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=timeout, limits=_SHARED_HTTP_LIMITS)


async def _request_with_general_client(
    method: str,
    url: str,
    *,
    timeout: float | httpx.Timeout | None = None,
    **kwargs,
) -> httpx.Response:
    if _general_http_client is not None:
        return await _general_http_client.request(method, url, timeout=timeout, **kwargs)
    async with httpx.AsyncClient() as ephemeral_client:
        return await ephemeral_client.request(method, url, timeout=timeout, **kwargs)


async def _validate_openrouter_key(raw_key: str) -> tuple[bool, str | None]:
    """Validate an OpenRouter key against an authenticated endpoint."""
    try:
        resp = await _request_with_general_client(
            "GET",
            "https://openrouter.ai/api/v1/key",
            headers={"Authorization": f"Bearer {raw_key}"},
            timeout=10.0,
        )
    except Exception as exc:
        logger.error("OpenRouter key validation request failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not reach OpenRouter to verify the key.") from exc

    if resp.status_code == 200:
        payload = resp.json()
        data = payload.get("data") if isinstance(payload, dict) else None
        if isinstance(data, dict):
            if data.get("disabled") is True:
                return False, "Key is disabled."
            return True, None
        return False, "OpenRouter returned an unexpected validation response."

    detail = None
    try:
        payload = resp.json()
        if isinstance(payload, dict):
            detail = payload.get("error", {}).get("message") or payload.get("message")
    except Exception:
        detail = None

    if resp.status_code in {401, 403}:
        return False, detail or "Key rejected by OpenRouter."
    if resp.status_code == 429:
        raise HTTPException(status_code=502, detail="OpenRouter rate-limited key validation. Try again in a moment.")
    raise HTTPException(
        status_code=502,
        detail=detail or f"OpenRouter validation failed with HTTP {resp.status_code}.",
    )


def _get_client_filter_date_range_bounds(value: str) -> tuple[int, int] | None:
    if not value:
        return None

    now = time.localtime()
    year = now.tm_year
    month = now.tm_mon

    def _epoch(y: int, m: int, d: int) -> int:
        return int(time.mktime((y, m, d, 0, 0, 0, 0, 0, -1)))

    if value == "this-week":
        current = time.localtime()
        days_from_monday = 6 if current.tm_wday == 6 else current.tm_wday
        start = int(time.time()) - days_from_monday * 86400
        start_tm = time.localtime(start)
        start_day = _epoch(start_tm.tm_year, start_tm.tm_mon, start_tm.tm_mday)
        end_day = start_day + (7 * 86400) - 1
        return start_day, end_day
    if value == "this-month":
        start_day = _epoch(year, month, 1)
        if month == 12:
            next_month = _epoch(year + 1, 1, 1)
        else:
            next_month = _epoch(year, month + 1, 1)
        return start_day, next_month - 1
    if value == "last-month":
        if month == 1:
            start_day = _epoch(year - 1, 12, 1)
            next_month = _epoch(year, 1, 1)
        else:
            start_day = _epoch(year, month - 1, 1)
            next_month = _epoch(year, month, 1)
        return start_day, next_month - 1
    if value == "this-year":
        return _epoch(year, 1, 1), _epoch(year + 1, 1, 1) - 1
    if value == "last-year":
        return _epoch(year - 1, 1, 1), _epoch(year, 1, 1) - 1
    return None


def _media_matches_client_filter_date_range(media: dict, value: str) -> bool:
    bounds = _get_client_filter_date_range_bounds(value)
    if not bounds:
        return True
    start_date = media.get("startDate") or {}
    if not start_date.get("year") or not start_date.get("month"):
        return False
    day = start_date.get("day") or 1
    media_epoch = int(time.mktime((start_date["year"], start_date["month"], day, 0, 0, 0, 0, 0, -1)))
    return bounds[0] <= media_epoch <= bounds[1]


def _sort_client_filtered_media(media_list: list[dict], sort: str) -> list[dict]:
    result = list(media_list)
    if sort == "TRENDING_DESC":
        result.sort(
            key=lambda m: (
                m.get("trendWindowScore") or 0,
                m.get("trendWindowPeak") or 0,
                m.get("trending") or 0,
                m.get("popularity") or 0,
            ),
            reverse=True,
        )
    elif sort == "SCORE_DESC":
        result.sort(key=lambda m: ((m.get("averageScore") or 0), (m.get("popularity") or 0)), reverse=True)
    elif sort == "START_DATE_DESC":
        result.sort(
            key=lambda m: (
                m.get("seasonYear") or 0,
                ((m.get("startDate") or {}).get("month") or 0),
                ((m.get("startDate") or {}).get("day") or 0),
                m.get("popularity") or 0,
            ),
            reverse=True,
        )
    elif sort == "FAVOURITES_DESC":
        result.sort(key=lambda m: ((m.get("favourites") or 0), (m.get("popularity") or 0)), reverse=True)
    else:
        result.sort(key=lambda m: ((m.get("popularity") or 0), (m.get("trending") or 0)), reverse=True)
    return result


def _apply_client_filters_to_media(media_list: list[dict], client_filters: dict | None) -> list[dict]:
    if not client_filters:
        return media_list
    client_filters = anilist.normalize_catalog_filters(client_filters)
    if not client_filters:
        return media_list

    genres = client_filters.get("genres") or []
    formats = client_filters.get("formats") or []
    statuses = client_filters.get("statuses") or []
    years = {str(y) for y in (client_filters.get("years") or [])}
    seasons = client_filters.get("seasons") or []
    daterange = client_filters.get("daterange") or ""
    min_score = client_filters.get("minScore") or 0
    sort = client_filters.get("sort") or "POPULARITY_DESC"

    result = media_list
    if genres:
        result = [m for m in result if all(g in (m.get("genres") or []) for g in genres)]
    if formats:
        result = [m for m in result if m.get("format") in formats]
    if statuses:
        result = [m for m in result if m.get("status") in statuses]
    if years:
        result = [m for m in result if str(m.get("seasonYear") or "") in years]
    if seasons:
        current_season, _ = anilist._season_now()
        resolved = {current_season if s == "CURRENT" else s for s in seasons}
        result = [m for m in result if m.get("season") in resolved]
    if daterange and not anilist.is_short_trend_daterange(daterange):
        result = [m for m in result if _media_matches_client_filter_date_range(m, daterange)]
    if min_score:
        result = [m for m in result if (m.get("averageScore") or 0) >= min_score]

    return _sort_client_filtered_media(result, sort)


async def _apply_client_filters_to_media_async(media_list: list[dict], client_filters: dict | None) -> list[dict]:
    if not client_filters:
        return media_list
    client_filters = anilist.normalize_catalog_filters(client_filters)
    if not client_filters:
        return media_list
    daterange = client_filters.get("daterange") or ""
    if not anilist.is_short_trend_daterange(daterange):
        return _apply_client_filters_to_media(media_list, client_filters)

    base_filters = dict(client_filters)
    base_filters.pop("daterange", None)
    sort = base_filters.pop("sort", client_filters.get("sort") or "POPULARITY_DESC")
    base_filtered = _apply_client_filters_to_media(media_list, base_filters)
    try:
        trend_filtered = await anilist.filter_media_by_trend_window(base_filtered, daterange)
    except Exception as exc:
        logger.warning("MediaTrend source filter failed; using unfiltered source fallback: %s", exc)
        trend_filtered = base_filtered
    return _sort_client_filtered_media(trend_filtered, sort)


def _media_title(media: dict | None) -> str:
    if not media:
        return "Unknown"
    title = media.get("title") or {}
    return title.get("english") or title.get("romaji") or title.get("native") or "Unknown"


def _catalog_requires_auth(catalog_config: dict | None, *, _depth: int = 0) -> bool:
    if _depth >= _MAX_CATALOG_NESTING:
        return True
    if not isinstance(catalog_config, dict):
        return False
    if catalog_config.get("type") in {"watching", "ai"}:
        return True
    base_catalog = catalog_config.get("baseCatalog")
    if isinstance(base_catalog, dict):
        return _catalog_requires_auth(base_catalog, _depth=_depth + 1)
    return False


def _normalize_media_ref(ref: dict | None) -> dict | None:
    if not isinstance(ref, dict):
        return None
    try:
        media_id = int(ref.get("id") or 0)
    except (TypeError, ValueError):
        media_id = 0
    title = str(ref.get("title") or "").strip()
    if media_id <= 0 and not title:
        return None
    normalized: dict[str, object] = {}
    if media_id > 0:
        normalized["id"] = media_id
    if title:
        normalized["title"] = title[:160]
    return normalized or None


async def _fetch_included_media_refs(included_media: list[dict] | None) -> list[dict]:
    normalized = [
        ref
        for ref in (_normalize_media_ref(item) for item in (included_media or []))
        if ref and ref.get("id")
    ]
    if not normalized:
        return []
    ordered_ids: list[int] = []
    seen_ids: set[int] = set()
    for ref in normalized:
        media_id = int(ref["id"])
        if media_id in seen_ids:
            continue
        seen_ids.add(media_id)
        ordered_ids.append(media_id)
    fetched = await anilist.get_media_by_ids(ordered_ids)
    by_id = {
        int(media.get("id")): media
        for media in fetched
        if isinstance(media, dict) and media.get("id")
    }
    return [by_id[media_id] for media_id in ordered_ids if media_id in by_id]


def _merge_media_lists(primary_media: list[dict], secondary_media: list[dict]) -> list[dict]:
    merged: list[dict] = []
    seen_ids: set[int] = set()
    for media in [*(primary_media or []), *(secondary_media or [])]:
        if not isinstance(media, dict):
            continue
        media_id = media.get("id")
        if not media_id or media_id in seen_ids:
            continue
        seen_ids.add(media_id)
        merged.append(media)
    return merged


def _normalize_ai_catalog_config(catalog_config: dict | None) -> dict:
    if not isinstance(catalog_config, dict):
        return {"aiMode": "legacy", "smartOptions": {}}
    mode = catalog_config.get("aiMode") if catalog_config.get("aiMode") in SMART_AI_MODES else "legacy"
    raw_options = catalog_config.get("smartOptions") if isinstance(catalog_config.get("smartOptions"), dict) else {}
    formats = [
        fmt for fmt in raw_options.get("formats", [])
        if isinstance(fmt, str) and fmt in SMART_AI_FORMATS
    ][:6]
    try:
        min_score = int(raw_options.get("minScore") or 0)
    except (TypeError, ValueError):
        min_score = 0
    min_score = max(0, min(100, min_score))
    popularity_bias = raw_options.get("popularityBias")
    if popularity_bias not in SMART_AI_POPULARITY_BIASES:
        popularity_bias = "balanced"
    normalized = {
        "aiMode": mode,
        "seedTitle": str(catalog_config.get("seedTitle") or "").strip()[:120],
        "smartOptions": {
            "formats": formats,
            "minScore": min_score,
            "popularityBias": popularity_bias,
        },
    }
    try:
        seed_id = int(catalog_config.get("seedMediaId") or 0)
    except (TypeError, ValueError):
        seed_id = 0
    if seed_id > 0:
        normalized["seedMediaId"] = seed_id
    return normalized


def _ai_catalog_cache_key(session_key: str, model: str, catalog_config: dict | None) -> str:
    normalized = _normalize_ai_catalog_config(catalog_config)
    payload = json.dumps(normalized, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha1(payload.encode("utf-8")).hexdigest()[:16]
    return f"ai_recs:{session_key}:{model}:{digest}"


async def _load_catalog_media(
    catalog_id: str,
    catalog_config: dict,
    page: int,
    *,
    auth_record: dict | None = None,
    session_key: str | None = None,
    _depth: int = 0,
) -> tuple[list[dict], int, float, int | None, bool, str]:
    """Load and client-filter raw AniList media for catalog routes and diagnostics."""
    if _depth >= _MAX_CATALOG_NESTING:
        raise HTTPException(status_code=400, detail="Catalog nesting too deep.")
    raw_media = None
    ttl = None
    should_cache = True
    catalog_kind = catalog_config.get("type") or ("preset" if catalog_id in PRESET_HANDLERS else "unknown")
    upstream_started_at = time.perf_counter()

    if catalog_id in PRESET_HANDLERS:
        raw_media = await PRESET_HANDLERS[catalog_id](page=page, per_page=PER_PAGE)
        ttl = TTL.get(catalog_id, 15 * 60)
    elif catalog_config.get("type") == "custom":
        base_catalog = catalog_config.get("baseCatalog") if isinstance(catalog_config.get("baseCatalog"), dict) else None
        included_media = catalog_config.get("includedMedia") if isinstance(catalog_config.get("includedMedia"), list) else []
        if base_catalog:
            base_id = str(base_catalog.get("id") or f"{catalog_id}-base")
            base_media, _, _, base_ttl, base_should_cache, base_kind = await _load_catalog_media(
                base_id,
                base_catalog,
                page,
                auth_record=auth_record,
                session_key=session_key,
                _depth=_depth + 1,
            )
            raw_media = list(base_media)
            ttl = base_ttl
            should_cache = base_should_cache
            catalog_kind = f"custom:{base_kind}"
        else:
            raw_media = await anilist.get_custom(catalog_config.get("filters", {}), page=page, per_page=PER_PAGE)
            ttl = 30 * 60
        if included_media and page == 1:
            extras = await _fetch_included_media_refs(included_media)
            if extras:
                raw_media = _merge_media_lists(extras, raw_media)
                if base_catalog and _catalog_requires_auth(base_catalog):
                    should_cache = False
    elif catalog_config.get("type") == "watching":
        if not auth_record:
            raise HTTPException(status_code=401, detail="Authentication required for watching list.")
        raw_token = _decrypt_anilist_token(auth_record)
        viewer = await anilist.get_viewer(raw_token)
        list_status = catalog_config.get("listStatus")
        if list_status == "FAVOURITES":
            raw_media = await anilist.get_favourites(raw_token, viewer["id"])
        else:
            raw_media = await anilist.get_watching_list(raw_token, viewer["id"], list_status or "CURRENT")
        should_cache = False
    elif catalog_config.get("type") == "ai":
        if not auth_record or not session_key:
            raise HTTPException(status_code=401, detail="Authentication required for AI recommendations.")
        raw_token = _decrypt_anilist_token(auth_record)
        encrypted_or = auth_record.get("encrypted_openrouter_key")
        if not encrypted_or:
            raise HTTPException(status_code=400, detail="OpenRouter API key not configured for this session.")
        try:
            or_key = decrypt(encrypted_or)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired OpenRouter session.")
        model = auth_record.get("openrouter_model") or "meta-llama/llama-3.3-70b-instruct"
        ai_cache_key = _ai_catalog_cache_key(session_key, model, catalog_config)
        ai_cached = cache.get(ai_cache_key)
        if ai_cached is not None:
            raw_media = ai_cached
        else:
            viewer = await anilist.get_viewer(raw_token)
            raw_media = await anilist.get_ai_recommendations(
                raw_token,
                viewer["id"],
                or_key,
                model,
                _normalize_ai_catalog_config(catalog_config),
            )
            cache.set(ai_cache_key, raw_media, 60 * 60)
        should_cache = False
    else:
        raise HTTPException(status_code=404, detail=f"Unknown catalog: {catalog_id}")

    raw_media = await _apply_client_filters_to_media_async(raw_media, catalog_config.get("clientFilters"))
    upstream_ms = (time.perf_counter() - upstream_started_at) * 1000
    return raw_media, len(raw_media), upstream_ms, ttl, should_cache, catalog_kind


async def _map_catalog_media(raw_media: list[dict]) -> dict:
    """Map media to external IDs and apply S1 replacements, retaining diagnostics."""
    id_map_started_at = time.perf_counter()
    id_mapping, replacements = await batch_map_ids(raw_media)
    id_map_ms = (time.perf_counter() - id_map_started_at) * 1000

    s1_fetch_ms = 0.0
    s1_fetch_failures = 0
    replacement_examples: list[dict] = []
    s1_media: dict[int, dict] = {}
    if replacements:
        s1_fetch_started_at = time.perf_counter()
        s1_ids = {s1_aid for s1_aid, _ in replacements.values()}
        existing_ids = {m["id"] for m in raw_media}
        fetch_ids = s1_ids - existing_ids
        if fetch_ids:
            id_list = list(fetch_ids)
            S1_BATCH = 12

            async def _fetch_s1_batch(batch: list[int]) -> None:
                if not batch:
                    return
                try:
                    for media in await anilist.get_media_by_ids(batch):
                        media_id = media.get("id")
                        if media_id:
                            s1_media[media_id] = media
                    return
                except Exception as exc:
                    if len(batch) == 1:
                        logger.warning("Failed to fetch S1 media id %s: %s", batch[0], exc)
                        return
                    logger.warning(
                        "Failed to fetch S1 media batch of %s items; retrying in smaller chunks: %s",
                        len(batch),
                        exc,
                    )
                    midpoint = max(1, len(batch) // 2)
                    await _fetch_s1_batch(batch[:midpoint])
                    await _fetch_s1_batch(batch[midpoint:])

            for batch_start in range(0, len(id_list), S1_BATCH):
                batch = id_list[batch_start:batch_start + S1_BATCH]
                await _fetch_s1_batch(batch)
            s1_fetch_ms = (time.perf_counter() - s1_fetch_started_at) * 1000

    canonical_media: list[dict] = []
    canonical_id_mapping: dict[int, str] = {}
    seen_canonical_ids: set[int] = set()
    raw_by_id = {m.get("id"): m for m in raw_media if m.get("id")}

    for media in raw_media:
        aid = media["id"]
        canonical_item = media
        canonical_aid = aid
        canonical_ext = id_mapping.get(aid)

        if aid in replacements:
            s1_aid, s1_ext = replacements[aid]
            replacement_media = raw_by_id.get(s1_aid) or s1_media.get(s1_aid)
            if len(replacement_examples) < _MAPPING_EXAMPLE_LIMIT:
                replacement_examples.append({
                    "fromTitle": _media_title(media),
                    "toTitle": _media_title(replacement_media) if replacement_media else f"AniList #{s1_aid}",
                })
            if replacement_media:
                canonical_item = replacement_media
                canonical_aid = s1_aid
                canonical_ext = s1_ext
            else:
                s1_fetch_failures += 1
                logger.warning("Missing canonical S1 media for AniList #%s -> #%s; returning original media", aid, s1_aid)

        if canonical_aid in seen_canonical_ids:
            continue

        seen_canonical_ids.add(canonical_aid)
        if canonical_ext is not None:
            canonical_id_mapping[canonical_aid] = canonical_ext
        canonical_media.append(canonical_item)

    return {
        "media": canonical_media,
        "id_mapping": canonical_id_mapping,
        "replacements": replacements,
        "id_map_ms": id_map_ms,
        "s1_fetch_ms": s1_fetch_ms,
        "s1_fetch_failures": s1_fetch_failures,
        "replacement_examples": replacement_examples,
    }

async def _fetch_catalog(
    catalog_id,
    catalog_config,
    page,
    auth_record: dict | None = None,
    session_key: str | None = None,
    poster_variant: str = "default",
    poster_base_url: str | None = None,
    poster_style: str = POSTER_LAB_DEFAULT_STYLE,
):
    started_at = time.perf_counter()
    cache_scope = json.dumps(catalog_config, sort_keys=True, separators=(",", ":"))
    cache_key = _poster_lab_cache_key(
        catalog_id,
        page,
        cache_scope=cache_scope,
        poster_variant=poster_variant,
        poster_base_url=poster_base_url,
        poster_style=poster_style,
    )
    fribb_warm_before = id_mapper.is_fribb_warm()
    cached = cache.get(cache_key)
    if cached is not None:
        total_ms = (time.perf_counter() - started_at) * 1000
        logger.info(
            "Catalog timing id=%s page=%s cache_hit=1 fribb_warm=%s total_ms=%.1f metas=%d",
            catalog_id,
            page,
            fribb_warm_before,
            total_ms,
            len(cached),
        )
        return cached

    raw_media, raw_count, upstream_ms, ttl, should_cache, catalog_kind = await _load_catalog_media(
        catalog_id,
        catalog_config,
        page,
        auth_record=auth_record,
        session_key=session_key,
    )
    mapped_result = await _map_catalog_media(raw_media)
    raw_media = mapped_result["media"]
    id_mapping = mapped_result["id_mapping"]
    fribb_warm_after = id_mapper.is_fribb_warm()
    top_labels_by_id = _poster_lab_top_labels(raw_media) if poster_variant == POSTER_LAB_VARIANT else {}

    meta_build_started_at = time.perf_counter()
    metas = []
    for media in raw_media:
        meta = anilist._media_to_meta(media, id_override=id_mapping.get(media["id"]))
        if poster_variant == POSTER_LAB_VARIANT and poster_base_url:
            poster_url = _poster_lab_poster_url(
                poster_base_url,
                media,
                style=poster_style,
                top_label=top_labels_by_id.get(media["id"]),
            )
            if poster_url:
                meta = {**meta, "poster": poster_url}
        metas.append(meta)
    meta_build_ms = (time.perf_counter() - meta_build_started_at) * 1000

    if should_cache and ttl:
        cache.set(cache_key, metas, ttl)
    total_ms = (time.perf_counter() - started_at) * 1000
    logger.info(
        "Catalog timing id=%s type=%s page=%s cache_hit=0 fribb_warm_before=%s fribb_warm_after=%s "
        "upstream_ms=%.1f id_map_ms=%.1f s1_fetch_ms=%.1f meta_build_ms=%.1f total_ms=%.1f raw_items=%d final_items=%d replacements=%d",
        catalog_id,
        catalog_kind,
        page,
        fribb_warm_before,
        fribb_warm_after,
        upstream_ms,
        mapped_result["id_map_ms"],
        mapped_result["s1_fetch_ms"],
        meta_build_ms,
        total_ms,
        raw_count,
        len(metas),
        len(mapped_result["replacements"]),
    )
    return metas

@asynccontextmanager
async def lifespan(app):
    global _anilist_http_client, _general_http_client
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
    _anilist_http_client = _build_shared_http_client(timeout=_ANILIST_HTTP_CLIENT_TIMEOUT)
    _general_http_client = _build_shared_http_client(timeout=_GENERAL_HTTP_CLIENT_TIMEOUT)
    anilist.configure_http_clients(
        anilist_client=_anilist_http_client,
        general_client=_general_http_client,
    )
    id_mapper.configure_http_client(_general_http_client)
    auth_store.initialize()
    logger.info("Durable auth store configured at %s", AUTH_DB_PATH)
    warmup_task = asyncio.create_task(id_mapper.warmup_indexes())
    try:
        try:
            warm = await asyncio.wait_for(asyncio.shield(warmup_task), timeout=_FRIBB_WARMUP_TIMEOUT)
            if warm:
                logger.info("Fribb/Kitsu warmup completed before startup")
            else:
                logger.warning("Fribb/Kitsu warmup finished without fresh data; continuing with fallback behavior")
        except asyncio.TimeoutError:
            logger.warning(
                "Fribb/Kitsu warmup still running after %.1fs; continuing startup",
                _FRIBB_WARMUP_TIMEOUT,
            )
        logger.info("AniList add-on starting on %s:%d — configure at /configure", HOST, PORT)
        yield
    finally:
        if not warmup_task.done():
            warmup_task.cancel()
            with suppress(asyncio.CancelledError):
                await warmup_task
        anilist.configure_http_clients()
        id_mapper.configure_http_client(None)
        if _anilist_http_client is not None:
            await _anilist_http_client.aclose()
            _anilist_http_client = None
        if _general_http_client is not None:
            await _general_http_client.aclose()
            _general_http_client = None

app = FastAPI(
    title="AniList Catalogs",
    version=MANIFEST["version"],
    lifespan=lifespan,
    docs_url="/docs" if ENABLE_API_DOCS else None,
    redoc_url="/redoc" if ENABLE_API_DOCS else None,
    openapi_url="/openapi.json" if ENABLE_API_DOCS else None,
)


def _request_path(request: Request) -> str:
    """Use the ASGI path, not Host-derived URL helpers, for security decisions."""
    path = request.scope.get("path")
    return path if isinstance(path, str) and path else "/"


def _declared_body_too_large(request: Request, max_bytes: int) -> bool:
    raw_length = request.headers.get("content-length")
    if raw_length is None:
        return False
    try:
        return int(raw_length) > max_bytes
    except ValueError:
        return True


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    path = _request_path(request)
    request.state.csp_nonce = secrets.token_urlsafe(16)

    if request.method == "OPTIONS":
        if _is_addon_route(path):
            response = Response(status_code=204)
            _apply_addon_cors(response)
            return response
        return Response(status_code=405)

    if (
        path.startswith("/api/")
        and request.method in {"POST", "PUT", "PATCH"}
        and _declared_body_too_large(request, _API_MAX_CONTENT_LENGTH)
    ):
        return JSONResponse(status_code=413, content={"detail": "Request body too large."})

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


@app.get("/static/{asset_name}", include_in_schema=False)
async def static_asset(asset_name: str):
    asset = _STATIC_ASSETS.get(asset_name)
    if asset is None:
        raise HTTPException(status_code=404, detail="Static asset not found")
    relative_path, media_type = asset
    asset_path = _STATIC_DIR / relative_path
    if not asset_path.is_file():
        raise HTTPException(status_code=404, detail="Static asset not found")
    return FileResponse(
        asset_path,
        media_type=media_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )

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

    resp = await _request_with_general_client(
        "POST",
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


def _normalize_session_key(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("session must be a string")
    session_key = value.strip()
    if not session_key:
        raise ValueError("session must not be empty")
    if len(session_key) > _MAX_SESSION_KEY_LENGTH:
        raise ValueError("session is too long")
    if not _SESSION_KEY_PATTERN.fullmatch(session_key):
        raise ValueError("session contains unsupported characters")
    return session_key


class _BoundedBody(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")


class _OptionalSessionBody(_BoundedBody):
    session: str | None = None

    @pydantic.field_validator("session", mode="before")
    @classmethod
    def _validate_optional_session(cls, value: str | None) -> str | None:
        return _normalize_session_key(value)


class _SessionKeyBody(_BoundedBody):
    session: str

    @pydantic.field_validator("session", mode="before")
    @classmethod
    def _validate_session(cls, value: str) -> str:
        session_key = _normalize_session_key(value)
        if session_key is None:
            raise ValueError("session must not be empty")
        return session_key


class _LogoutBody(_OptionalSessionBody):
    pass

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
        resp = await _request_with_general_client(
            "POST",
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
    # Store the encrypted token in durable server-side storage and hand the
    # client a short auth key. This keeps the full token out of the manifest URL.
    session_key = secrets.token_urlsafe(16)  # 22 URL-safe characters, 128 bits of entropy
    auth_store.upsert_auth(session_key, encrypted)
    # Do not log the raw access_token — only the encrypted form is safe to emit.
    logger.info("OAuth login successful; durable auth key stored, redirecting to /configure")
    response = RedirectResponse(url=f"/configure#s={session_key}")
    _clear_oauth_state_cookie(response)
    return response


@app.post("/oauth/logout", include_in_schema=False)
async def oauth_logout(body: _LogoutBody):
    # Revoke durable auth state when the user explicitly disconnects.
    if body.session:
        auth_store.delete_auth(body.session)
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

_AUTH_401 = {"detail": "Session not found or revoked."}

def _migrate_legacy_session(session_key: str, *, touch_last_used: bool = False) -> dict | None:
    """Persist a still-live legacy in-memory session into SQLite on first use."""
    encrypted = cache.get(f"session:{session_key}")
    if not encrypted:
        return None
    or_data = cache.get(f"session_or:{session_key}")
    encrypted_or = None
    or_model = None
    if isinstance(or_data, dict):
        encrypted_or = or_data.get("encrypted_key")
        or_model = or_data.get("model")
    auth_store.upsert_auth(
        session_key,
        encrypted,
        encrypted_openrouter_key=encrypted_or,
        openrouter_model=or_model,
    )
    logger.info("Migrated live legacy auth key into SQLite store")
    return auth_store.get_auth(session_key, touch_last_used=touch_last_used)


def _resolve_auth(session_key: str, *, touch_last_used: bool = True) -> dict:
    """Resolve a durable auth record, falling back to live legacy cache data once."""
    record = auth_store.get_auth(session_key, touch_last_used=touch_last_used)
    if record is None:
        record = _migrate_legacy_session(session_key, touch_last_used=touch_last_used)
    if not record:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])
    return record


def _decrypt_anilist_token(auth_record: dict) -> str:
    """Decrypt the AniList token from an auth record with a uniform 401 on failure."""
    try:
        return decrypt(auth_record["encrypted_anilist_token"])
    except InvalidToken:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])


def _resolve_session(session_key: str) -> str:
    """Look up and decrypt an AniList token via the durable auth store."""
    return _decrypt_anilist_token(_resolve_auth(session_key))

class _SessionBody(_SessionKeyBody):
    pass

def _validate_small_json_object(value: dict | None, *, name: str) -> dict | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be JSON serializable") from exc
    if len(encoded.encode("utf-8")) > _MAX_AI_CATALOG_CONFIG_BYTES:
        raise ValueError(f"{name} is too large")
    return value


class _PreviewAiBody(_SessionKeyBody):
    catalog: dict | None = None
    client_filters: dict | None = None

    @pydantic.field_validator("catalog")
    @classmethod
    def _validate_catalog_size(cls, value: dict | None) -> dict | None:
        return _validate_small_json_object(value, name="catalog config")

    @pydantic.field_validator("client_filters")
    @classmethod
    def _validate_client_filters(cls, value: dict | None) -> dict | None:
        return _validate_small_json_object(value, name="client filters")

_VALID_LIST_STATUSES = {"CURRENT", "PLANNING", "COMPLETED", "PAUSED", "DROPPED", "REPEATING", "FAVOURITES"}

class _PreviewWatchingBody(_SessionKeyBody):
    list_status: str
    client_filters: dict | None = None

    @pydantic.field_validator("list_status", mode="before")
    @classmethod
    def _validate_list_status(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("list_status must be a string")
        normalized = value.strip().upper()
        if len(normalized) > 24:
            raise ValueError("list_status is too long")
        return normalized

    @pydantic.field_validator("client_filters")
    @classmethod
    def _validate_client_filters(cls, value: dict | None) -> dict | None:
        return _validate_small_json_object(value, name="client filters")


class _PreviewCustomBody(_BoundedBody):
    filters: dict = pydantic.Field(default_factory=dict)

    @pydantic.field_validator("filters")
    @classmethod
    def _validate_filters(cls, value: dict | None) -> dict:
        return _validate_small_json_object(value or {}, name="filters") or {}

_ALLOWED_MODELS = {
    "meta-llama/llama-3.3-70b-instruct",
    "google/gemini-flash-1.5",
    "openai/gpt-4o-mini",
    "anthropic/claude-haiku-4-5-20251001",
}
# Custom models must match org/model-name format (alphanumeric, hyphens, dots, underscores).
_MODEL_PATTERN = re.compile(r"^[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+$")

class _SaveOrKeyBody(_SessionKeyBody):
    key: str | None = None   # None means "keep existing key, just update model"
    model: str = "meta-llama/llama-3.3-70b-instruct"

    @pydantic.field_validator("key", mode="before")
    @classmethod
    def _validate_optional_key(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("key must be a string")
        if len(value) > _MAX_OPENROUTER_KEY_LENGTH:
            raise ValueError("key is too long")
        return value

    @pydantic.field_validator("model", mode="before")
    @classmethod
    def _validate_model(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("model must be a string")
        model = value.strip()
        if not model:
            raise ValueError("model must not be empty")
        if len(model) > 128:
            raise ValueError("model identifier too long")
        return model

class _TestOrKeyBody(_BoundedBody):
    key: str

    @pydantic.field_validator("key", mode="before")
    @classmethod
    def _validate_key(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("key must be a string")
        if len(value) > _MAX_OPENROUTER_KEY_LENGTH:
            raise ValueError("key is too long")
        return value

@app.post("/api/preview-watching")
async def api_preview_watching(request: Request, body: _PreviewWatchingBody):
    """Return the authenticated user's watching list or favourites for the configure UI preview.

    Uses a durable auth key (never the raw AniList token). Rate-limited per IP
    to prevent auth-key enumeration.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")
    if body.list_status not in _VALID_LIST_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid list_status.")
    raw_token = _decrypt_anilist_token(_resolve_auth(body.session))
    try:
        viewer = await anilist.get_viewer(raw_token)
        if body.list_status == "FAVOURITES":
            media = await anilist.get_favourites(raw_token, viewer["id"])
        else:
            media = await anilist.get_watching_list(raw_token, viewer["id"], body.list_status)
        media = await _apply_client_filters_to_media_async(media, body.client_filters)
    except Exception as exc:
        logger.error("preview_watching failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch list from AniList.")
    return {"media": media}

@app.post("/api/save-openrouter-key")
async def api_save_openrouter_key(request: Request, body: _SaveOrKeyBody):
    """Store (or update) the user's OpenRouter API key in durable auth storage.

    The key is Fernet-encrypted before being written to the auth store —
    it is never returned in any response or written to any log.
    When *key* is None, only the model preference is updated (key unchanged).
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")

    session_key = body.session
    auth_record = _resolve_auth(session_key)

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
        is_valid, detail = await _validate_openrouter_key(raw_key)
        if not is_valid:
            raise HTTPException(status_code=400, detail=detail or "Key rejected by OpenRouter.")
        encrypted_or = encrypt(raw_key)
    else:
        # No new key — preserve existing, update model only.
        encrypted_or = auth_record.get("encrypted_openrouter_key")
        if not encrypted_or:
            raise HTTPException(status_code=400, detail="No OpenRouter key stored for this session. Provide a key.")

    auth_store.update_openrouter(
        session_key,
        encrypted_openrouter_key=encrypted_or,
        openrouter_model=model,
    )
    cache.delete_prefix(f"ai_recs:{session_key}:")
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

    is_valid, detail = await _validate_openrouter_key(raw_key)
    if is_valid:
        return {"valid": True}
    return JSONResponse(status_code=400, content={"valid": False, "detail": detail or "Key rejected by OpenRouter."})


@app.post("/api/preview-ai")
async def api_preview_ai(request: Request, body: _PreviewAiBody):
    """Return AI-recommended anime as raw AniList media dicts for the configure UI.

    Uses the same 1-hour per-auth-key cache as the Stremio catalog route to avoid
    redundant (slow, expensive) AI calls.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")

    session_key = body.session
    auth_record = _resolve_auth(session_key)
    raw_token = _decrypt_anilist_token(auth_record)

    encrypted_or = auth_record.get("encrypted_openrouter_key")
    if not encrypted_or:
        raise HTTPException(status_code=400, detail="OpenRouter API key not configured. Add it via the AI settings.")

    try:
        or_key = decrypt(encrypted_or)
    except Exception:
        raise HTTPException(status_code=401, detail=_AUTH_401["detail"])

    model = auth_record.get("openrouter_model") or "meta-llama/llama-3.3-70b-instruct"

    # Check cache first — keyed on session + model so switching models triggers fresh recs.
    catalog_config = body.catalog if isinstance(body.catalog, dict) else {"type": "ai"}
    if catalog_config.get("type") not in {None, "ai"}:
        raise HTTPException(status_code=400, detail="Invalid AI catalog.")
    catalog_config = {**catalog_config, "type": "ai"}

    ai_cache_key = _ai_catalog_cache_key(session_key, model, catalog_config)
    cached = cache.get(ai_cache_key)
    if cached is not None:
        media = await _apply_client_filters_to_media_async(cached, body.client_filters)
        return {"media": media}

    try:
        viewer = await anilist.get_viewer(raw_token)
        raw_media = await anilist.get_ai_recommendations(
            raw_token,
            viewer["id"],
            or_key,
            model,
            _normalize_ai_catalog_config(catalog_config),
        )
    except anilist.AIRecommendationError as exc:
        logger.error("preview_ai failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc) or "AI recommendation request failed.")
    except Exception as exc:
        logger.error("preview_ai failed: %s", exc)
        raise HTTPException(status_code=502, detail="AI recommendation request failed.")

    cache.set(ai_cache_key, raw_media, 60 * 60)
    media = await _apply_client_filters_to_media_async(raw_media, body.client_filters)
    return {"media": media}


@app.post("/api/preview-custom")
async def api_preview_custom(request: Request, body: _PreviewCustomBody):
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")
    try:
        media = await anilist.get_custom(body.filters or {}, page=1, per_page=PER_PAGE)
    except Exception as exc:
        logger.error("preview_custom failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not preview AniList filters.")
    return {"media": media}


@app.get("/api/search-anime")
async def api_search_anime(request: Request, q: str = ""):
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")
    query = str(q or "").strip()
    if len(query) < 3:
        raise HTTPException(status_code=400, detail="Query must be at least 3 characters.")
    if len(query) > 120:
        raise HTTPException(status_code=400, detail="Query must be at most 120 characters.")
    try:
        media = await anilist.search_anime(query, limit=SEARCH_RESULT_LIMIT)
    except Exception as exc:
        logger.error("search_anime failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not search AniList.") from exc
    compact_media = []
    for item in media[:SEARCH_RESULT_LIMIT]:
        compact_media.append(
            {
                "id": item.get("id"),
                "title": _media_title(item),
                "coverImage": ((item.get("coverImage") or {}).get("extraLarge") or (item.get("coverImage") or {}).get("large") or ""),
                "genres": item.get("genres") or [],
                "format": item.get("format") or "",
                "seasonYear": item.get("seasonYear") or ((item.get("startDate") or {}).get("year")),
            }
        )
    return {"media": compact_media}


@app.post("/api/me")
async def api_me(request: Request, body: _SessionBody):
    """Return the authenticated user's display name and avatar URL.

    Accepts a short auth key in the POST body. The key is looked up in the
    server-side auth store to retrieve the encrypted AniList token — the
    token itself never travels to the client after the initial OAuth exchange.
    """
    ip = request.client.host if request.client else "unknown"
    if not _check_session_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests.")
    auth_record = _resolve_auth(body.session)
    raw_token = _decrypt_anilist_token(auth_record)
    try:
        viewer = await anilist.get_viewer(raw_token)
    except Exception as exc:
        logger.error("get_viewer failed: %s", exc)
        raise HTTPException(status_code=502, detail="Could not fetch user from AniList.")
    return {
        "name": viewer["name"],
        "avatar": viewer["avatar"],
        "has_or_key": auth_record.get("encrypted_openrouter_key") is not None,
        "or_model": auth_record.get("openrouter_model"),
    }

@app.get("/manifest.json")
async def manifest_default(): return JSONResponse(_build_manifest(DEFAULT_CONFIG))

@app.get("/{config_segment}/manifest.json")
async def manifest_configured(config_segment: str):
    config_token, _ = _parse_config_segment(config_segment)
    return JSONResponse(_build_manifest(decode_config(config_token)))

@app.get("/{config_segment}/poster-lab/manifest.json")
async def manifest_configured_poster_lab(config_segment: str):
    config_token, _ = _parse_config_segment(config_segment)
    return JSONResponse(_build_manifest(decode_config(config_token), poster_variant=POSTER_LAB_VARIANT))


async def _catalog_response(
    request: Request,
    config_segment: str,
    content_type: str,
    catalog_id: str,
    skip: int = 0,
    *,
    poster_variant: str = "default",
):
    if content_type != "series":
        raise HTTPException(status_code=404, detail="Unsupported content type")
    config_token, session_key = _parse_config_segment(config_segment)
    config = decode_config(config_token)
    catalog_config = next((c for c in config.get("catalogs", []) if c["id"] == catalog_id), None)
    if catalog_config is None:
        raise HTTPException(status_code=404, detail=f"Catalog not in config: {catalog_id}")
    page = _skip_to_page(skip)

    auth_record: dict | None = None
    if _catalog_requires_auth(catalog_config):
        if not session_key:
            if config.get("legacy_auth_manifest"):
                raise HTTPException(
                    status_code=410,
                    detail="This manifest uses an old embedded AniList session. Reconnect AniList and reinstall the addon.",
                )
            raise HTTPException(status_code=401, detail="Authentication required for this catalog.")
        auth_record = _resolve_auth(session_key)

    poster_base_url = _poster_lab_base_url(request) if poster_variant == POSTER_LAB_VARIANT else None
    poster_style = _poster_lab_normalize_style(config.get("posterStyle") or config.get("poster_style"))
    try:
        metas = await _fetch_catalog(
            catalog_id,
            catalog_config,
            page,
            auth_record=auth_record,
            session_key=session_key,
            poster_variant=poster_variant,
            poster_base_url=poster_base_url,
            poster_style=poster_style,
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Fetch failed for %s: %s", catalog_id, exc)
        raise HTTPException(status_code=502, detail="AniList API error") from exc
    if catalog_config.get("randomize"):
        metas = _stable_shuffle_metas(
            metas,
            config_token=config_token,
            catalog_id=catalog_id,
            page=page,
        )
    return JSONResponse({"metas": metas})

@app.get("/{config_segment}/catalog/{content_type}/{catalog_id}.json")
@app.get("/{config_segment}/catalog/{content_type}/{catalog_id}/skip={skip}.json")
async def catalog_configured(request: Request, config_segment: str, content_type: str, catalog_id: str, skip: int = 0):
    return await _catalog_response(request, config_segment, content_type, catalog_id, skip)

@app.get("/{config_segment}/poster-lab/catalog/{content_type}/{catalog_id}.json")
@app.get("/{config_segment}/poster-lab/catalog/{content_type}/{catalog_id}/skip={skip}.json")
async def catalog_configured_poster_lab(request: Request, config_segment: str, content_type: str, catalog_id: str, skip: int = 0):
    return await _catalog_response(
        request,
        config_segment,
        content_type,
        catalog_id,
        skip,
        poster_variant=POSTER_LAB_VARIANT,
    )

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

@app.get("/{config_segment}/poster-lab/meta/{content_type}/{item_id}.json")
async def meta_configured_poster_lab(config_segment: str, content_type: str, item_id: str):
    return await meta_configured(config_segment, content_type, item_id)

@app.get("/catalog/{content_type}/{catalog_id}.json")
@app.get("/catalog/{content_type}/{catalog_id}/skip={skip}.json")
async def catalog_legacy(request: Request, content_type: str, catalog_id: str, skip: int = 0):
    return await catalog_configured(request, DEFAULT_CONFIG_TOKEN, content_type, catalog_id, skip)

@app.get("/meta/{content_type}/{item_id}.json")
async def meta_legacy(content_type: str, item_id: str):
    return await meta_configured(DEFAULT_CONFIG_TOKEN, content_type, item_id)

@app.get("/poster-lab/render.png")
async def poster_lab_render(
    src: str,
    top: str = "",
    bottom: str = "",
    badge: str = "",
    style: str = POSTER_LAB_DEFAULT_STYLE,
    v: str = POSTER_LAB_VERSION,
):
    del v  # cache-busting hook for poster design iterations
    if not _poster_lab_allow_source(src):
        raise HTTPException(status_code=400, detail="Unsupported poster source host.")
    try:
        image = await _render_poster_lab_image(
            src,
            top[:64],
            bottom[:36],
            badge[:7] or None,
            style=_poster_lab_normalize_style(style),
        )
    except HTTPException as exc:
        logger.warning("Poster banners fallback for %s: %s", src, exc.detail)
        return RedirectResponse(url=src, status_code=307)
    return Response(
        content=image,
        media_type="image/png",
        headers={"Cache-Control": "public, max-age=21600"},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=HOST, port=PORT, reload=False)
