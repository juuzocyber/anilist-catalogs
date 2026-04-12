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

    prompt_completed = sorted(completed, key=_entry_sort_key, reverse=True)[:AI_PROMPT_COMPLETED_LIMIT]
    prompt_watching = sorted(watching, key=_entry_sort_key, reverse=True)[:AI_PROMPT_WATCHING_LIMIT]
    prompt_entries = prompt_completed + prompt_watching
    if not prompt_entries:
        prompt_entries = sorted(seen_entries, key=_entry_sort_key, reverse=True)[:AI_PROMPT_COMPLETED_LIMIT]

    # 2. Build exclusion sets from the full seen history.
    seen_titles: set[str] = set()
    seen_ids: set[int] = set()
    for entry in seen_entries:
        m = entry["media"]
        seen_titles.update(_title_variants(m))
        if m.get("id"):
            seen_ids.add(m["id"])

    completed_text = ", ".join(_format_history_entry(entry) for entry in prompt_completed)
    watching_text = ", ".join(_format_history_entry(entry) for entry in prompt_watching)
    if not completed_text:
        completed_text = ", ".join(_format_history_entry(entry) for entry in prompt_entries)
    if not watching_text:
        watching_text = "None"

    # 3. POST to OpenRouter - ask for more titles than we need so strict filtering
    # still leaves a healthy unseen list.
    system_prompt = (
        "You are an anime recommendation engine. "
        "Return only a valid JSON array of anime title strings. "
        "Use official English or Romaji titles. "
        "No explanation, no IDs, only the JSON array of strings."
    )
    user_prompt = (
        f"Based on this AniList history, recommend {AI_MODEL_CANDIDATE_COUNT} anime the user has not seen. "
        "Treat completed anime as the strongest signal and currently watching anime as a secondary signal. "
        "Do not recommend anything already in completed, current, paused, dropped, or repeating. "
        "Focus on titles similar in genre, tone, and quality to their highest-rated completed entries. "
        "Return only a JSON array of anime title strings.\n\n"
        f"Completed history (strongest signal): {completed_text}\n\n"
        f"Currently watching (secondary signal): {watching_text}"
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
                    "max_tokens": 4096,
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
        seed_entries = prompt_completed or prompt_entries
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
                    f"nodes {{ mediaRecommendation {{ {MEDIA_FIELDS} isAdult }} }} "
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
