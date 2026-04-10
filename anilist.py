"""
AniList GraphQL client.
"""

import re
import httpx
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger(__name__)
ANILIST_URL = "https://graphql.anilist.co"

MEDIA_FIELDS = """
    id
    idMal
    title { romaji english native }
    coverImage { extraLarge large color }
    bannerImage
    description(asHtml: false)
    season
    seasonYear
    startDate { year month day }
    endDate { year month day }
    episodes
    status
    averageScore
    meanScore
    popularity
    genres
    format
    siteUrl
"""

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
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(
            ANILIST_URL,
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
                {MEDIA_FIELDS}
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
                    id idMal title { romaji english native }
                    coverImage { extraLarge large color }
                    bannerImage description(asHtml: false)
                    season seasonYear
                    startDate { year month day } endDate { year month day }
                    episodes status averageScore meanScore popularity genres format siteUrl isAdult
                }
            }
        }
    }
    """
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
            media(type: ANIME sort: TRENDING_DESC isAdult: false) {{ {MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, {"page": page, "perPage": per_page})
    return data["Page"]["media"]

async def get_top_rated(page: int = 1, per_page: int = 30) -> list[dict]:
    query = f"""
    query ($page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(type: ANIME sort: SCORE_DESC isAdult: false format_in: [TV, TV_SHORT, MOVIE, OVA, ONA]) {{ {MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, {"page": page, "perPage": per_page})
    return data["Page"]["media"]

async def get_custom(filters: dict, page: int = 1, per_page: int = 30) -> list[dict]:
    args = ["type: ANIME", "isAdult: false"]
    variables: dict = {"page": page, "perPage": per_page}

    if filters.get("genres"):
        args.append("genre_in: $genres")
        variables["genres"] = filters["genres"]
    if filters.get("year"):
        args.append("seasonYear: $year")
        variables["year"] = int(filters["year"])
    if filters.get("season"):
        args.append("season: $season")
        variables["season"] = filters["season"]
    if filters.get("format"):
        args.append("format: $format")
        variables["format"] = filters["format"]
    if filters.get("status"):
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

    sort = filters.get("sort", "POPULARITY_DESC")
    _VALID_SORTS = {"POPULARITY_DESC", "TRENDING_DESC", "SCORE_DESC", "START_DATE_DESC", "FAVOURITES_DESC"}
    if sort not in _VALID_SORTS:
        sort = "POPULARITY_DESC"
    args.append(f"sort: {sort}")

    var_decls = "$page: Int, $perPage: Int"
    if "genres"   in variables: var_decls += ", $genres: [String]"
    if "year"     in variables: var_decls += ", $year: Int"
    if "season"   in variables: var_decls += ", $season: MediaSeason"
    if "format"   in variables: var_decls += ", $format: MediaFormat"
    if "status"   in variables: var_decls += ", $status: MediaStatus"
    if "minScore" in variables: var_decls += ", $minScore: Int"
    if "sdGt"     in variables: var_decls += ", $sdGt: FuzzyDateInt"
    if "sdLt"     in variables: var_decls += ", $sdLt: FuzzyDateInt"

    query = f"""
    query ({var_decls}) {{
        Page(page: $page, perPage: $perPage) {{
            media({" ".join(args)}) {{ {MEDIA_FIELDS} }}
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
                        {MEDIA_FIELDS}
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
                        {MEDIA_FIELDS}
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
    token: str, user_id: int, status: str,
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
                        {MEDIA_FIELDS}
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
) -> list[dict]:
    """Return AI-recommended anime based on the user's watch history.

    Fetches completed + currently-watching titles with personal scores, asks the
    LLM to recommend anime by **title** (not ID — LLMs don't know AniList IDs),
    then batch-searches AniList to resolve titles into media dicts.

    Returns raw AniList media dicts (same shape as MEDIA_FIELDS — apply
    _media_to_meta in the caller).  Never logs the openrouter_key.
    """
    import asyncio as _asyncio
    import json as _json
    import re as _re

    # 1. Fetch completed + currently-watching history with user scores
    try:
        completed = await _fetch_history_with_scores(anilist_token, user_id, "COMPLETED")
        watching  = await _fetch_history_with_scores(anilist_token, user_id, "CURRENT")
    except Exception as exc:
        logger.error("AI recs: failed to fetch watch history: %s", exc)
        return []

    all_entries = (completed + watching)[:50]
    if not all_entries:
        logger.warning("AI recs: no watch history found, returning empty list")
        return []

    # 2. Format as compact text — prefer user score, fall back to community average
    parts = []
    seen_titles: set[str] = set()
    seen_ids: set[int] = set()
    for entry in all_entries:
        m = entry["media"]
        title = (
            (m.get("title") or {}).get("english")
            or (m.get("title") or {}).get("romaji")
            or "Unknown"
        )
        user_score = entry["user_score"]
        if user_score:
            score_str = f"{user_score}/10"
        else:
            avg = m.get("averageScore") or m.get("meanScore")
            score_str = f"~{avg // 10}/10" if avg else "?"
        parts.append(f"{title} ({score_str})")
        # Track ALL title variants for dedup — the LLM may recommend by any name
        for key in ("english", "romaji", "native"):
            t = (m.get("title") or {}).get(key)
            if t:
                seen_titles.add(t.lower().strip())
        if m.get("id"):
            seen_ids.add(m["id"])
    history_text = ", ".join(parts)

    # 3. POST to OpenRouter — ask for titles, not IDs
    system_prompt = (
        "You are an anime recommendation engine. "
        "Return only a valid JSON array of anime title strings. "
        "Use official English or Romaji titles. "
        "No explanation, no IDs, only the JSON array of strings."
    )
    user_prompt = (
        "Based on this watch history, recommend 50 anime the user hasn't seen. "
        "Focus on titles similar in genre, tone, and quality to their highest-rated entries. "
        "Return only a JSON array of anime title strings.\n\n"
        f"Watch history: {history_text}"
    )
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
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
                    "max_tokens": 2048,
                },
            )
        if resp.status_code != 200:
            logger.error("AI recs: OpenRouter returned HTTP %d", resp.status_code)
            return []
        payload = resp.json()
    except Exception as exc:
        logger.error("AI recs: OpenRouter request failed: %s", exc)
        return []

    # 4. Parse JSON array of title strings from the model's response
    try:
        content = (payload.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
        match = _re.search(r"\[[\s\S]*\]", content)
        if not match:
            logger.error("AI recs: no JSON array in model response (first 200 chars): %s", content[:200])
            return []
        raw_titles = _json.loads(match.group(0))
        if not isinstance(raw_titles, list):
            logger.error("AI recs: parsed value is not a list")
            return []
        candidate_titles: list[str] = []
        seen_in_resp: set[str] = set()
        for item in raw_titles:
            if not isinstance(item, str) or not item.strip():
                continue
            normalized = item.strip()
            key = normalized.lower()
            if key not in seen_in_resp and key not in seen_titles:
                candidate_titles.append(normalized)
                seen_in_resp.add(key)
        if len(candidate_titles) > 50:
            candidate_titles = candidate_titles[:50]
    except Exception as exc:
        logger.error("AI recs: failed to parse OpenRouter response: %s", exc)
        return []

    if not candidate_titles:
        logger.warning("AI recs: no valid candidate titles extracted")
        return []

    # 5. Batch-search AniList for titles using aliased queries (10 per batch)
    async def _search_batch(titles: list[str]) -> list[dict]:
        """Search multiple anime titles in a single AniList query using aliases."""
        alias_parts = []
        for i, title in enumerate(titles):
            safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
            alias_parts.append(
                f'a{i}: Media(search: "{safe_title}", type: ANIME, isAdult: false) '
                f"{{ {MEDIA_FIELDS} }}"
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
    for batch in batches:
        try:
            results = await _search_batch(batch)
            for media in results:
                mid = media["id"]
                if mid not in seen_ids and mid not in found_ids:
                    all_media.append(media)
                    found_ids.add(mid)
        except Exception as exc:
            logger.warning("AI recs: AniList search batch failed: %s", exc)
            continue
        if len(all_media) >= 50:
            break

    if not all_media:
        logger.warning("AI recs: no valid media found from title search")
        return []

    return all_media[:50]


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
