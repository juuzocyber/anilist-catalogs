"""
AniList GraphQL client.
"""

import asyncio
import json
import logging
import re
import unicodedata
from datetime import datetime, timezone, timedelta
from typing import Optional

import httpx

logger = logging.getLogger(__name__)
ANILIST_URL = "https://graphql.anilist.co"
_anilist_http_client: httpx.AsyncClient | None = None
_general_http_client: httpx.AsyncClient | None = None


class AIRecommendationError(Exception):
    """Raised when upstream AI recommendation generation fails."""

MEDIA_FIELDS = """
    id
    idMal
    title { romaji english native }
    coverImage { extraLarge large color }
    bannerImage
    description(asHtml: false)
    source(version: 2)
    season
    seasonYear
    startDate { year month day }
    endDate { year month day }
    episodes
    status
    averageScore
    meanScore
    popularity
    trending
    genres
    format
    siteUrl
    nextAiringEpisode { episode timeUntilAiring }
    rankings { rank type allTime context }
    relations { edges { relationType(version: 2) node { type } } }
    studios(isMain: true) { nodes { name } }
"""
CATALOG_MEDIA_FIELDS = MEDIA_FIELDS + "\n    isAdult"

AI_HISTORY_MEDIA_FIELDS = """
    id
    title { romaji english native }
    averageScore
    meanScore
    popularity
"""

AI_RECOMMENDATION_TARGET = 50
AI_RECOMMENDATION_MINIMUM = 30
AI_MODEL_CANDIDATE_COUNT = 100
AI_PROMPT_COMPLETED_LIMIT = 80
AI_PROMPT_WATCHING_LIMIT = 20
AI_EXCLUSION_STATUSES = ("COMPLETED", "CURRENT", "PAUSED", "DROPPED", "REPEATING")
SMART_AI_MODES = {"title_seed", "top_rated", "hidden_completed"}
SMART_AI_FORMATS = {"TV", "TV_SHORT", "MOVIE", "OVA", "ONA", "SPECIAL"}
SMART_AI_POPULARITY_BIASES = {"balanced", "hidden", "mainstream"}


def configure_http_clients(
    *,
    anilist_client: httpx.AsyncClient | None = None,
    general_client: httpx.AsyncClient | None = None,
) -> None:
    """Install shared outbound clients for hot paths.

    When unset, the module falls back to short-lived clients so direct calls
    outside FastAPI lifespan still work.
    """
    global _anilist_http_client, _general_http_client
    _anilist_http_client = anilist_client
    _general_http_client = general_client


async def _request_with_client(
    shared_client: httpx.AsyncClient | None,
    method: str,
    url: str,
    *,
    timeout: float | httpx.Timeout | None = None,
    **kwargs,
) -> httpx.Response:
    if shared_client is not None:
        return await shared_client.request(method, url, timeout=timeout, **kwargs)
    async with httpx.AsyncClient() as ephemeral_client:
        return await ephemeral_client.request(method, url, timeout=timeout, **kwargs)

def _season_now():
    now = datetime.now(timezone.utc)
    month = now.month
    year = now.year
    if month in (1, 2, 3):   season = "WINTER"
    elif month in (4, 5, 6): season = "SPRING"
    elif month in (7, 8, 9): season = "SUMMER"
    else:                     season = "FALL"
    return season, year

def _week_bounds_unix():
    now = datetime.now(timezone.utc)
    monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    sunday = (monday + timedelta(days=6)).replace(hour=23, minute=59, second=59)
    return int(monday.timestamp()), int(sunday.timestamp())


def _normalize_title_key(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).casefold()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def _title_variants(media: dict) -> set[str]:
    variants: set[str] = set()
    for key in ("english", "romaji", "native"):
        title = (media.get("title") or {}).get(key)
        if title:
            normalized = _normalize_title_key(title)
            if normalized:
                variants.add(normalized)
    return variants


def _entry_sort_key(entry: dict) -> tuple[int, int, int]:
    media = entry["media"]
    user_score = entry.get("user_score") or 0
    community_score = media.get("averageScore") or media.get("meanScore") or 0
    popularity = media.get("popularity") or 0
    return (user_score, community_score, popularity)


def _format_history_entry(entry: dict) -> str:
    media = entry["media"]
    title = (
        (media.get("title") or {}).get("english")
        or (media.get("title") or {}).get("romaji")
        or (media.get("title") or {}).get("native")
        or "Unknown"
    )
    user_score = entry.get("user_score") or 0
    if user_score:
        score_str = f"{user_score}/10"
    else:
        avg = media.get("averageScore") or media.get("meanScore")
        score_str = f"~{avg // 10}/10" if avg else "?"
    return f"{title} ({score_str})"


def _media_display_title(media: dict | None) -> str:
    if not media:
        return "Unknown"
    title = media.get("title") or {}
    return title.get("english") or title.get("romaji") or title.get("native") or "Unknown"


def _normalize_smart_config(smart_config: dict | None) -> dict:
    """Return the small, public-safe AI row config used by prompts/cache keys."""
    if not isinstance(smart_config, dict):
        return {"aiMode": "legacy", "smartOptions": {}}
    mode = smart_config.get("aiMode") if smart_config.get("aiMode") in SMART_AI_MODES else "legacy"
    raw_options = smart_config.get("smartOptions") if isinstance(smart_config.get("smartOptions"), dict) else {}
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
    result = {
        "aiMode": mode,
        "seedTitle": str(smart_config.get("seedTitle") or "").strip()[:120],
        "smartOptions": {
            "formats": formats,
            "minScore": min_score,
            "popularityBias": popularity_bias,
        },
    }
    try:
        seed_id = int(smart_config.get("seedMediaId") or 0)
    except (TypeError, ValueError):
        seed_id = 0
    if seed_id > 0:
        result["seedMediaId"] = seed_id
    return result


def _smart_option_instruction(options: dict) -> str:
    parts: list[str] = []
    formats = options.get("formats") or []
    if formats:
        parts.append("Prefer these formats when possible: " + ", ".join(formats) + ".")
    min_score = options.get("minScore") or 0
    if min_score:
        parts.append(f"Prefer titles with AniList community score at least {min_score} when possible.")
    bias = options.get("popularityBias") or "balanced"
    if bias == "hidden":
        parts.append("Prefer less obvious, lower-popularity picks over the most famous titles.")
    elif bias == "mainstream":
        parts.append("Prefer recognizable, easy-to-recommend titles with strong mainstream appeal.")
    return " ".join(parts)


def _media_matches_smart_options(media: dict, options: dict) -> bool:
    formats = options.get("formats") or []
    if formats and media.get("format") not in formats:
        return False
    min_score = options.get("minScore") or 0
    if min_score and (media.get("averageScore") or media.get("meanScore") or 0) < min_score:
        return False
    return True


def _build_ai_recommendation_prompts(
    completed: list[dict],
    watching: list[dict],
    seen_entries: list[dict],
    smart_config: dict | None = None,
    *,
    seed_media: dict | None = None,
) -> tuple[str, str, list[dict], list[dict]]:
    """Build the model prompts plus seed entries used by the fallback graph."""
    config = _normalize_smart_config(smart_config)
    mode = config["aiMode"]
    options = config["smartOptions"]

    prompt_completed = sorted(completed, key=_entry_sort_key, reverse=True)[:AI_PROMPT_COMPLETED_LIMIT]
    prompt_watching = sorted(watching, key=_entry_sort_key, reverse=True)[:AI_PROMPT_WATCHING_LIMIT]
    prompt_entries = prompt_completed + prompt_watching
    if not prompt_entries:
        prompt_entries = sorted(seen_entries, key=_entry_sort_key, reverse=True)[:AI_PROMPT_COMPLETED_LIMIT]

    completed_text = ", ".join(_format_history_entry(entry) for entry in prompt_completed)
    watching_text = ", ".join(_format_history_entry(entry) for entry in prompt_watching) or "None"
    if not completed_text:
        completed_text = ", ".join(_format_history_entry(entry) for entry in prompt_entries)

    seed_entries = prompt_completed or prompt_entries
    option_text = _smart_option_instruction(options)
    intent = (
        f"Based on this AniList history, recommend {AI_MODEL_CANDIDATE_COUNT} anime the user has not seen. "
        "Treat completed anime as the strongest signal and currently watching anime as a secondary signal. "
        "Focus on titles similar in genre, tone, and quality to their highest-rated completed entries. "
    )

    if mode == "title_seed":
        seed_title = config.get("seedTitle") or _media_display_title(seed_media)
        if not seed_title or seed_title == "Unknown":
            seed_title = "the selected seed anime"
        intent = (
            f"Recommend {AI_MODEL_CANDIDATE_COUNT} anime the user has not seen that feel meaningfully similar to "
            f"{seed_title}. Use the user's AniList history as taste calibration, but make the selected seed the "
            "primary signal for genre, tone, pacing, themes, and audience fit. "
        )
        if seed_media and seed_media.get("id"):
            seed_entries = [{"media": seed_media, "user_score": 10}]
    elif mode == "top_rated":
        top_rated = [entry for entry in completed if (entry.get("user_score") or 0) >= 10]
        if not top_rated:
            top_rated = [entry for entry in completed if (entry.get("user_score") or 0) >= 9]
        top_rated = sorted(top_rated or completed, key=_entry_sort_key, reverse=True)[:25]
        top_text = ", ".join(_format_history_entry(entry) for entry in top_rated) or completed_text
        intent = (
            f"Recommend {AI_MODEL_CANDIDATE_COUNT} anime the user has not seen based primarily on their highest-rated "
            "completed anime. Treat this 10/10 or near-10/10 set as the strongest taste signal. "
            f"Top-rated completed entries: {top_text}. "
        )
        seed_entries = top_rated or seed_entries
    elif mode == "hidden_completed":
        hidden_seeds = sorted(completed, key=_entry_sort_key, reverse=True)[:40]
        hidden_text = ", ".join(_format_history_entry(entry) for entry in hidden_seeds) or completed_text
        intent = (
            f"Recommend {AI_MODEL_CANDIDATE_COUNT} anime the user has not seen as hidden gems inferred from their "
            "completed list. Avoid obvious top-of-all-time picks when a more specific, high-quality fit exists. "
            f"Completed taste signals: {hidden_text}. "
        )
        seed_entries = hidden_seeds or seed_entries

    system_prompt = (
        "You are an anime recommendation engine. "
        "Return only a valid JSON array of anime title strings. "
        "Use official English or Romaji titles. "
        "No explanation, no IDs, only the JSON array of strings."
    )
    user_prompt = (
        intent
        + "Do not recommend anything already in completed, current, paused, dropped, or repeating. "
        + option_text
        + " Return only a JSON array of anime title strings.\n\n"
        + f"Completed history: {completed_text}\n\n"
        + f"Currently watching: {watching_text}"
    )
    return system_prompt, user_prompt, seed_entries, prompt_completed

# Season suffixes to strip when an AniList entry maps to a tt (IMDB) ID.
# IMDB treats multi-season anime as one show, so "JUJUTSU KAISEN Season 3"
# should become "JUJUTSU KAISEN" when served with a tt ID.
_SEASON_SUFFIX_RE = re.compile(
    r'\s+(?:'
    r'Season\s+\d+'                     # Season 2, Season 12
    r'|\d+(?:st|nd|rd|th)\s+Season'     # 2nd Season, 3rd Season
    r'|Part\s+\d+'                      # Part 2
    r'|Cour\s+\d+'                      # Cour 2
    r'|(?:VIII|VII|VI|IV|III|II)'        # Roman numerals II–VIII (longest first)
    r')(?:[:\s].*)?$',                  # also strip trailing subtitles (": Foo Bar")
    re.IGNORECASE,
)

def _media_to_meta(media: dict, *, id_override: str | None = None) -> dict:
    title = (
        media.get("title", {}).get("english")
        or media.get("title", {}).get("romaji")
        or media.get("title", {}).get("native")
        or "Unknown"
    )
    # When mapped to a TMDB or IMDB ID, strip season suffixes — both treat
    # the whole show as one entry so "Season 3" is misleading.
    if id_override and (id_override.startswith("tmdb:") or id_override.startswith("tt")):
        title = _SEASON_SUFFIX_RE.sub('', title).strip()
    start = media.get("startDate") or {}
    end = media.get("endDate") or {}
    if start.get("year") and end.get("year") and start["year"] != end["year"]:
        release_info = f"{start['year']}–{end['year']}"
    elif start.get("year"):
        release_info = str(start["year"])
    else:
        release_info = None
    score = media.get("averageScore") or media.get("meanScore")
    imdb_rating = f"{score / 10:.1f}" if score else None
    cover = media.get("coverImage") or {}
    poster = cover.get("extraLarge") or cover.get("large")
    return {
        "id": id_override or f"anilist:{media['id']}",
        "type": "series",
        "name": title,
        "poster": poster,
        "posterShape": "poster",
        "background": media.get("bannerImage"),
        "description": media.get("description") or None,
        "releaseInfo": release_info,
        "imdbRating": imdb_rating,
        "genres": media.get("genres") or [],
        "website": media.get("siteUrl"),
    }

async def _gql(query: str, variables: dict, *, token: str | None = None) -> dict:
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    resp = await _request_with_client(
        _anilist_http_client,
        "POST",
        ANILIST_URL,
        timeout=10.0,
        json={"query": query, "variables": variables},
        headers=headers,
    )
    resp.raise_for_status()
    payload = resp.json()
    if "errors" in payload:
        logger.error("AniList GraphQL errors: %s", payload["errors"])
        raise ValueError(f"AniList error: {payload['errors']}")
    return payload["data"]

async def get_popular_season(page: int = 1, per_page: int = 30) -> list[dict]:
    season, year = _season_now()
    query = f"""
    query ($season: MediaSeason, $year: Int, $page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(season: $season seasonYear: $year type: ANIME sort: POPULARITY_DESC isAdult: false) {{
                {CATALOG_MEDIA_FIELDS}
            }}
        }}
    }}
    """
    data = await _gql(query, {"season": season, "year": year, "page": page, "perPage": per_page})
    return data["Page"]["media"]

async def get_airing_week(page: int = 1, per_page: int = 50) -> list[dict]:
    start, end = _week_bounds_unix()
    query = """
    query ($start: Int, $end: Int, $page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            airingSchedules(airingAt_greater: $start airingAt_lesser: $end sort: TIME) {
                airingAt episode
                media {
                    %s
                }
            }
        }
    }
    """ % CATALOG_MEDIA_FIELDS
    data = await _gql(query, {"start": start, "end": end, "page": page, "perPage": per_page})
    seen: set[int] = set()
    unique_media = []
    for s in data["Page"]["airingSchedules"]:
        m = s["media"]
        if m["id"] not in seen and not m.get("isAdult"):
            seen.add(m["id"])
            unique_media.append(m)
    unique_media.sort(key=lambda m: m.get("popularity") or 0, reverse=True)
    return unique_media

async def get_trending(page: int = 1, per_page: int = 30) -> list[dict]:
    query = f"""
    query ($page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(type: ANIME sort: TRENDING_DESC isAdult: false) {{ {CATALOG_MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, {"page": page, "perPage": per_page})
    return data["Page"]["media"]

async def get_top_rated(page: int = 1, per_page: int = 30) -> list[dict]:
    query = f"""
    query ($page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(type: ANIME sort: SCORE_DESC isAdult: false format_in: [TV, TV_SHORT, MOVIE, OVA, ONA]) {{ {CATALOG_MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, {"page": page, "perPage": per_page})
    return data["Page"]["media"]


async def search_anime(query_text: str, limit: int = 8) -> list[dict]:
    search = str(query_text or "").strip()
    if len(search) < 3:
        return []
    safe_limit = max(1, min(int(limit or 8), 20))
    query = f"""
    query ($search: String, $page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(search: $search, type: ANIME, isAdult: false, sort: POPULARITY_DESC) {{
                {CATALOG_MEDIA_FIELDS}
            }}
        }}
    }}
    """
    data = await _gql(query, {"search": search, "page": 1, "perPage": safe_limit})
    return (data.get("Page") or {}).get("media") or []

async def get_custom(filters: dict, page: int = 1, per_page: int = 30) -> list[dict]:
    args = ["type: ANIME", "isAdult: false"]
    variables: dict = {"page": page, "perPage": per_page}

    if filters.get("genres"):
        args.append("genre_in: $genres")
        variables["genres"] = filters["genres"]
    years = filters.get("years") if isinstance(filters.get("years"), list) else None
    year_value = years[0] if years and len(years) == 1 else filters.get("year")
    if year_value:
        args.append("seasonYear: $year")
        variables["year"] = int(year_value)
    seasons = filters.get("seasons") if isinstance(filters.get("seasons"), list) else None
    season_value = seasons[0] if seasons and len(seasons) == 1 else filters.get("season")
    if season_value:
        resolved_season = season_value
        resolved_year = None
        if season_value == "CURRENT":
            resolved_season, resolved_year = _season_now()
        args.append("season: $season")
        variables["season"] = resolved_season
        if resolved_year is not None and "year" not in variables:
            args.append("seasonYear: $year")
            variables["year"] = resolved_year
    if filters.get("formats"):
        args.append("format_in: $formats")
        variables["formats"] = filters["formats"]
    elif filters.get("format"):
        args.append("format: $format")
        variables["format"] = filters["format"]
    if filters.get("statuses"):
        args.append("status_in: $statuses")
        variables["statuses"] = filters["statuses"]
    elif filters.get("status"):
        args.append("status: $status")
        variables["status"] = filters["status"]
    if filters.get("minScore"):
        args.append("averageScore_greater: $minScore")
        variables["minScore"] = int(filters["minScore"])
    if filters.get("month") and filters.get("year"):
        y, m = int(filters["year"]), int(filters["month"])
        variables["sdGt"] = y * 10000 + m * 100 - 1
        nm = 1 if m == 12 else m + 1
        ny = y + 1 if m == 12 else y
        variables["sdLt"] = ny * 10000 + nm * 100
        args.append("startDate_greater: $sdGt")
        args.append("startDate_lesser: $sdLt")
    elif filters.get("daterange"):
        now = datetime.now(timezone.utc)
        year = now.year
        month = now.month
        value = str(filters["daterange"])
        start = end = None
        if value == "this-month":
            start = datetime(year, month, 1, tzinfo=timezone.utc)
            end = datetime(year + (1 if month == 12 else 0), 1 if month == 12 else month + 1, 1, tzinfo=timezone.utc) - timedelta(days=1)
        elif value == "last-month":
            start_month = 12 if month == 1 else month - 1
            start_year = year - 1 if month == 1 else year
            start = datetime(start_year, start_month, 1, tzinfo=timezone.utc)
            end = datetime(year, month, 1, tzinfo=timezone.utc) - timedelta(days=1)
        elif value == "this-year":
            start = datetime(year, 1, 1, tzinfo=timezone.utc)
            end = datetime(year, 12, 31, tzinfo=timezone.utc)
        elif value == "last-year":
            start = datetime(year - 1, 1, 1, tzinfo=timezone.utc)
            end = datetime(year - 1, 12, 31, tzinfo=timezone.utc)
        elif value == "this-week":
            monday = (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            start = monday
            end = monday + timedelta(days=6)
        if start and end:
            prev_day = start - timedelta(days=1)
            variables["sdGt"] = prev_day.year * 10000 + prev_day.month * 100 + (prev_day.day or 1)
            next_end = end + timedelta(days=1)
            variables["sdLt"] = next_end.year * 10000 + next_end.month * 100 + (next_end.day or 1)
            args.append("startDate_greater: $sdGt")
            args.append("startDate_lesser: $sdLt")

    sort = filters.get("sort", "POPULARITY_DESC")
    _VALID_SORTS = {"POPULARITY_DESC", "TRENDING_DESC", "SCORE_DESC", "START_DATE_DESC", "FAVOURITES_DESC"}
    if sort not in _VALID_SORTS:
        sort = "POPULARITY_DESC"
    args.append(f"sort: {sort}")

    var_decls = "$page: Int, $perPage: Int"
    if "genres"   in variables: var_decls += ", $genres: [String]"
    if "year"     in variables: var_decls += ", $year: Int"
    if "season"   in variables: var_decls += ", $season: MediaSeason"
    if "formats"  in variables: var_decls += ", $formats: [MediaFormat]"
    if "format"   in variables: var_decls += ", $format: MediaFormat"
    if "statuses" in variables: var_decls += ", $statuses: [MediaStatus]"
    if "status"   in variables: var_decls += ", $status: MediaStatus"
    if "minScore" in variables: var_decls += ", $minScore: Int"
    if "sdGt"     in variables: var_decls += ", $sdGt: FuzzyDateInt"
    if "sdLt"     in variables: var_decls += ", $sdLt: FuzzyDateInt"

    query = f"""
    query ({var_decls}) {{
        Page(page: $page, perPage: $perPage) {{
            media({" ".join(args)}) {{ {CATALOG_MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, variables)
    return data["Page"]["media"]

async def get_viewer(token: str) -> dict:
    """Return the authenticated user's id, name, and avatar URL.

    *token* is the raw (decrypted) AniList Bearer token — never log it.
    """
    query = """
    query {
        Viewer {
            id
            name
            avatar { large }
        }
    }
    """
    data = await _gql(query, {}, token=token)
    viewer = data["Viewer"]
    return {
        "id":     viewer["id"],
        "name":   viewer["name"],
        "avatar": (viewer.get("avatar") or {}).get("large"),
    }


async def get_watching_list(token: str, user_id: int, list_status: str = "CURRENT") -> list[dict]:
    """Return an authenticated user's anime list filtered by status.

    *token* is the raw (decrypted) AniList Bearer token — never log it.
    *list_status* matches AniList MediaListStatus: CURRENT, PLANNING, COMPLETED,
    PAUSED, DROPPED, or REPEATING.
    Returns raw AniList media dicts — callers apply _media_to_meta as needed.
    """
    query = f"""
    query ($userId: Int, $status: MediaListStatus) {{
        MediaListCollection(userId: $userId, type: ANIME, status: $status) {{
            lists {{
                entries {{
                    media {{
                        {CATALOG_MEDIA_FIELDS}
                    }}
                }}
            }}
        }}
    }}
    """
    data = await _gql(query, {"userId": user_id, "status": list_status}, token=token)
    media_list: list[dict] = []
    for lst in (data.get("MediaListCollection") or {}).get("lists") or []:
        for entry in lst.get("entries") or []:
            media = entry.get("media")
            if media:
                media_list.append(media)
    return media_list


async def get_favourites(token: str, user_id: int) -> list[dict]:
    """Return the authenticated user's favourite anime.

    Favourites live under User.favourites.anime.nodes, not MediaListCollection.
    *token* is the raw (decrypted) AniList Bearer token — never log it.
    Returns raw AniList media dicts — callers apply _media_to_meta as needed.
    """
    query = f"""
    query ($userId: Int) {{
        User(id: $userId) {{
            favourites {{
                anime {{
                    nodes {{
                        {CATALOG_MEDIA_FIELDS}
                    }}
                }}
            }}
        }}
    }}
    """
    data = await _gql(query, {"userId": user_id}, token=token)
    nodes = (
        (data.get("User") or {})
        .get("favourites", {})
        .get("anime", {})
        .get("nodes") or []
    )
    return nodes


async def _fetch_history_with_scores(
    token: str,
    user_id: int,
    status: str,
    media_fields: str = AI_HISTORY_MEDIA_FIELDS,
) -> list[dict]:
    """Fetch user's anime list with personal scores for AI recommendation context.

    Returns dicts with ``media`` (raw AniList media dict) and ``user_score``
    (the user's own score, 0 if unset).  Never log *token*.
    """
    query = f"""
    query ($userId: Int, $status: MediaListStatus) {{
        MediaListCollection(userId: $userId, type: ANIME, status: $status) {{
            lists {{
                entries {{
                    score(format: POINT_10)
                    media {{
                        {media_fields}
                    }}
                }}
            }}
        }}
    }}
    """
    data = await _gql(query, {"userId": user_id, "status": status}, token=token)
    results: list[dict] = []
    for lst in (data.get("MediaListCollection") or {}).get("lists") or []:
        for entry in lst.get("entries") or []:
            media = entry.get("media")
            if media:
                results.append({
                    "media": media,
                    "user_score": entry.get("score") or 0,
                })
    return results


async def get_ai_recommendations(
    anilist_token: str,
    user_id: int,
    openrouter_key: str,
    model: str = "meta-llama/llama-3.3-70b-instruct",
    smart_config: dict | None = None,
) -> list[dict]:
    """Return AI-recommended anime based on the user's watch history.

    Fetches completed + currently-watching titles with personal scores, asks the
    LLM to recommend anime by **title** (not ID — LLMs don't know AniList IDs),
    then batch-searches AniList to resolve titles into media dicts.

    Returns raw AniList media dicts (same shape as MEDIA_FIELDS — apply
    _media_to_meta in the caller).  Never logs the openrouter_key.
    """
    # 1. Fetch watch history with user scores. Completed/current shape the prompt,
    # while the broader seen set prevents already-watched titles from leaking back.
    try:
        history_lists = await asyncio.gather(*[
            _fetch_history_with_scores(anilist_token, user_id, status)
            for status in AI_EXCLUSION_STATUSES
        ])
    except Exception as exc:
        logger.error("AI recs: failed to fetch watch history: %s", exc)
        return []

    history_by_status = dict(zip(AI_EXCLUSION_STATUSES, history_lists))
    completed = history_by_status.get("COMPLETED", [])
    watching = history_by_status.get("CURRENT", [])
    seen_entries = [
        entry
        for status in AI_EXCLUSION_STATUSES
        for entry in history_by_status.get(status, [])
    ]

    if not seen_entries:
        logger.warning("AI recs: no watch history found, returning empty list")
        return []

    # 2. Build exclusion sets from the full seen history.
    seen_titles: set[str] = set()
    seen_ids: set[int] = set()
    for entry in seen_entries:
        m = entry["media"]
        seen_titles.update(_title_variants(m))
        if m.get("id"):
            seen_ids.add(m["id"])

    config = _normalize_smart_config(smart_config)
    seed_media = None
    seed_id = config.get("seedMediaId")
    if config.get("aiMode") == "title_seed" and seed_id:
        try:
            seed_media = await get_media_by_id(seed_id, media_fields=AI_HISTORY_MEDIA_FIELDS)
        except Exception as exc:
            logger.warning("AI recs: failed to fetch seed media %s: %s", seed_id, exc)
            seed_media = None
        if seed_media and seed_media.get("id"):
            seen_ids.add(seed_media["id"])
            seen_titles.update(_title_variants(seed_media))

    # 3. POST to OpenRouter - ask for more titles than we need so strict filtering
    # still leaves a healthy unseen list.
    system_prompt, user_prompt, seed_entries, prompt_completed = _build_ai_recommendation_prompts(
        completed,
        watching,
        seen_entries,
        config,
        seed_media=seed_media,
    )
    smart_options = config.get("smartOptions") or {}
    try:
        resp = await _request_with_client(
            _general_http_client,
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
            timeout=30.0,
            headers={
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                "temperature": 0.7,
                "max_tokens": 4096,
            },
        )
        if resp.status_code != 200:
            detail = None
            try:
                payload = resp.json()
                if isinstance(payload, dict):
                    detail = payload.get("error", {}).get("message") or payload.get("message")
            except Exception:
                detail = None
            logger.error("AI recs: OpenRouter returned HTTP %d detail=%s", resp.status_code, detail)
            raise AIRecommendationError(detail or f"OpenRouter returned HTTP {resp.status_code}")
        payload = resp.json()
    except Exception as exc:
        if isinstance(exc, AIRecommendationError):
            raise
        logger.error("AI recs: OpenRouter request failed: %s", exc)
        raise AIRecommendationError("Could not reach OpenRouter.")

    # 4. Parse JSON array of title strings from the model's response
    try:
        content = (payload.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
        match = re.search(r"\[[\s\S]*\]", content)
        if not match:
            logger.error("AI recs: no JSON array in model response (first 200 chars): %s", content[:200])
            return []
        raw_titles = json.loads(match.group(0))
        if not isinstance(raw_titles, list):
            logger.error("AI recs: parsed value is not a list")
            return []
        candidate_titles: list[str] = []
        seen_in_resp: set[str] = set()
        for item in raw_titles:
            if not isinstance(item, str) or not item.strip():
                continue
            normalized = item.strip()
            key = _normalize_title_key(normalized)
            if not key:
                continue
            if key not in seen_in_resp and key not in seen_titles:
                candidate_titles.append(normalized)
                seen_in_resp.add(key)
        if len(candidate_titles) > AI_MODEL_CANDIDATE_COUNT:
            candidate_titles = candidate_titles[:AI_MODEL_CANDIDATE_COUNT]
    except Exception as exc:
        logger.error("AI recs: failed to parse OpenRouter response: %s", exc)
        return []

    if not candidate_titles:
        logger.warning("AI recs: no valid candidate titles extracted")
        return []

    # 5. Batch-search AniList for titles using aliased queries (10 per batch).
    async def _search_batch(titles: list[str]) -> list[dict]:
        """Search multiple anime titles in a single AniList query using aliases."""
        alias_parts = []
        for i, title in enumerate(titles):
            safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
            alias_parts.append(
                f'a{i}: Media(search: "{safe_title}", type: ANIME, isAdult: false) '
                f"{{ {CATALOG_MEDIA_FIELDS} }}"
            )
        query = "query {\n" + "\n".join(alias_parts) + "\n}"
        data = await _gql(query, {})
        results = []
        for i in range(len(titles)):
            media = data.get(f"a{i}")
            if media and isinstance(media, dict) and media.get("id"):
                results.append(media)
        return results

    batch_size = 10
    batches = [
        candidate_titles[i : i + batch_size]
        for i in range(0, len(candidate_titles), batch_size)
    ]

    all_media: list[dict] = []
    found_ids: set[int] = set()
    found_titles: set[str] = set()
    for batch in batches:
        try:
            results = await _search_batch(batch)
            for media in results:
                mid = media["id"]
                title_keys = _title_variants(media)
                if mid in seen_ids or mid in found_ids:
                    continue
                if title_keys & seen_titles:
                    continue
                if title_keys and title_keys & found_titles:
                    continue
                if not _media_matches_smart_options(media, smart_options):
                    continue
                all_media.append(media)
                found_ids.add(mid)
                found_titles.update(title_keys)
        except Exception as exc:
            logger.warning("AI recs: AniList search batch failed: %s", exc)
            continue
        if len(all_media) >= AI_RECOMMENDATION_TARGET:
            break

    # 6. If the model leaves us short after strict filtering, fill the gap using
    # AniList's own recommendation graph seeded from the user's strongest history.
    if len(all_media) < AI_RECOMMENDATION_MINIMUM:
        seed_entries = seed_entries or prompt_completed
        seed_ids = [
            entry["media"]["id"]
            for entry in seed_entries
            if entry.get("media") and entry["media"].get("id")
        ]

        async def _recommendation_batch(seed_batch: list[int]) -> list[dict]:
            alias_parts = []
            for i, media_id in enumerate(seed_batch):
                alias_parts.append(
                    f"a{i}: Media(id: {media_id}, type: ANIME) {{ "
                    f"recommendations(sort: RATING_DESC, perPage: 12) {{ "
                    f"nodes {{ mediaRecommendation {{ {CATALOG_MEDIA_FIELDS} }} }} "
                    f"}} }}"
                )
            data = await _gql("query {\n" + "\n".join(alias_parts) + "\n}", {})
            fallback_results: list[dict] = []
            for i in range(len(seed_batch)):
                media = data.get(f"a{i}") or {}
                nodes = (media.get("recommendations") or {}).get("nodes") or []
                for node in nodes:
                    candidate = node.get("mediaRecommendation")
                    if candidate and candidate.get("id") and not candidate.get("isAdult"):
                        fallback_results.append(candidate)
            return fallback_results

        for start in range(0, len(seed_ids), 5):
            try:
                fallback_results = await _recommendation_batch(seed_ids[start : start + 5])
            except Exception as exc:
                logger.warning("AI recs: AniList recommendation fallback failed: %s", exc)
                continue
            for media in fallback_results:
                mid = media["id"]
                title_keys = _title_variants(media)
                if mid in seen_ids or mid in found_ids:
                    continue
                if title_keys & seen_titles:
                    continue
                if title_keys and title_keys & found_titles:
                    continue
                if not _media_matches_smart_options(media, smart_options):
                    continue
                all_media.append(media)
                found_ids.add(mid)
                found_titles.update(title_keys)
                if len(all_media) >= AI_RECOMMENDATION_TARGET:
                    break
            if len(all_media) >= AI_RECOMMENDATION_TARGET:
                break

    if not all_media:
        logger.warning("AI recs: no valid media found from title search")
        return []

    return all_media[:AI_RECOMMENDATION_TARGET]


async def get_media_by_id(anilist_id: int, media_fields: str = MEDIA_FIELDS) -> Optional[dict]:
    query = f"""
    query ($id: Int) {{
        Media(id: $id, type: ANIME) {{
            {media_fields}
        }}
    }}
    """
    data = await _gql(query, {"id": anilist_id})
    media = data.get("Media")
    return media if isinstance(media, dict) else None


async def get_media_by_ids(anilist_ids: list[int], media_fields: str = CATALOG_MEDIA_FIELDS) -> list[dict]:
    if not anilist_ids:
        return []

    alias_parts = [
        f"a{i}: Media(id: {anilist_id}, type: ANIME) {{ {media_fields} }}"
        for i, anilist_id in enumerate(anilist_ids)
    ]
    data = await _gql("query {\n" + "\n".join(alias_parts) + "\n}", {})
    media_items: list[dict] = []
    for i in range(len(anilist_ids)):
        media = data.get(f"a{i}")
        if media and isinstance(media, dict) and media.get("id"):
            media_items.append(media)
    return media_items


async def get_meta(anilist_id: int) -> Optional[dict]:
    query = f"""
    query ($id: Int) {{
        Media(id: $id, type: ANIME) {{
            {MEDIA_FIELDS}
            trailer {{ id site thumbnail }}
            externalLinks {{ url site type }}
            studios(isMain: true) {{ nodes {{ name siteUrl }} }}
        }}
    }}
    """
    data = await _gql(query, {"id": anilist_id})
    media = data.get("Media")
    if not media:
        return None
    meta = _media_to_meta(media)
    trailer = media.get("trailer")
    if trailer and trailer.get("site") == "youtube":
        meta["trailers"] = [{"source": trailer["id"], "type": "Trailer"}]
    links = [{"name": "AniList", "category": "AniList", "url": media.get("siteUrl", "")}]
    for ext in media.get("externalLinks") or []:
        if ext.get("type") in ("STREAMING", "INFO"):
            links.append({"name": ext["site"], "category": ext["type"].title(), "url": ext["url"]})
    meta["links"] = links
    studios = (media.get("studios") or {}).get("nodes") or []
    if studios:
        meta["director"] = studios[0]["name"]
    return meta
