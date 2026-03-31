"""
AniList GraphQL client.
"""

import httpx
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional

logger = logging.getLogger(__name__)
ANILIST_URL = "https://graphql.anilist.co"

MEDIA_FIELDS = """
    id
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

def _media_to_meta(media: dict) -> dict:
    title = (
        media.get("title", {}).get("english")
        or media.get("title", {}).get("romaji")
        or media.get("title", {}).get("native")
        or "Unknown"
    )
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
        "id": f"anilist:{media['id']}",
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
    return [_media_to_meta(m) for m in data["Page"]["media"]]

async def get_airing_week(page: int = 1, per_page: int = 50) -> list[dict]:
    start, end = _week_bounds_unix()
    query = """
    query ($start: Int, $end: Int, $page: Int, $perPage: Int) {
        Page(page: $page, perPage: $perPage) {
            airingSchedules(airingAt_greater: $start airingAt_lesser: $end sort: TIME) {
                airingAt episode
                media {
                    id title { romaji english native }
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
    return [_media_to_meta(m) for m in unique_media]

async def get_trending(page: int = 1, per_page: int = 30) -> list[dict]:
    query = f"""
    query ($page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(type: ANIME sort: TRENDING_DESC isAdult: false) {{ {MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, {"page": page, "perPage": per_page})
    return [_media_to_meta(m) for m in data["Page"]["media"]]

async def get_top_rated(page: int = 1, per_page: int = 30) -> list[dict]:
    query = f"""
    query ($page: Int, $perPage: Int) {{
        Page(page: $page, perPage: $perPage) {{
            media(type: ANIME sort: SCORE_DESC isAdult: false format_in: [TV, TV_SHORT, MOVIE, OVA, ONA]) {{ {MEDIA_FIELDS} }}
        }}
    }}
    """
    data = await _gql(query, {"page": page, "perPage": per_page})
    return [_media_to_meta(m) for m in data["Page"]["media"]]

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
    return [_media_to_meta(m) for m in data["Page"]["media"]]

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


async def get_watching_list(token: str, user_id: int, list_status: str = "CURRENT", *, raw: bool = False) -> list[dict]:
    """Return an authenticated user's anime list filtered by status.

    *token* is the raw (decrypted) AniList Bearer token — never log it.
    *list_status* matches AniList MediaListStatus: CURRENT, PLANNING, COMPLETED,
    PAUSED, DROPPED, or REPEATING.
    When *raw* is True, returns the unprocessed AniList media dicts instead of
    Stremio meta dicts (used by the configure UI preview).
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
    return media_list if raw else [_media_to_meta(m) for m in media_list]


async def get_favourites(token: str, user_id: int, *, raw: bool = False) -> list[dict]:
    """Return the authenticated user's favourite anime.

    Favourites live under User.favourites.anime.nodes, not MediaListCollection.
    *token* is the raw (decrypted) AniList Bearer token — never log it.
    When *raw* is True, returns the unprocessed AniList media dicts instead of
    Stremio meta dicts (used by the configure UI preview).
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
    return nodes if raw else [_media_to_meta(m) for m in nodes]


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
