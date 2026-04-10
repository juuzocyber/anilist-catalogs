"""
ID mapping layer: AniList -> TMDB/IMDB via Fribb + Kitsu IMDb supplement.

Resolution chain (per anime entry):
1. Fribb (in-memory, no API call): season.tvdb == 1 -> imdb/tmdb ID.
   season.tvdb > 1 -> trace S1 via shared tvdb_id.
2. Slug prefix match (in-memory): anime-planet_id slug starts with an S1 slug.
3. Kitsu supplement (in-memory): if a matched Fribb entry still has no imdb/tmdb
   ID, use Fribb's kitsu_id to look up an IMDb ID from a supplemental mapping.

Lookup uses both anilist_id and mal_id indexes because Fribb's anilist_id
can be stale for entries that were merged/renumbered on AniList.

ID preference: IMDb > TMDB > AniList fallback.
"""

import logging
import time

import httpx

from cache import cache

logger = logging.getLogger(__name__)

FRIBB_URL = "https://raw.githubusercontent.com/Fribb/anime-lists/master/anime-list-full.json"
KITSU_IMDB_URL = "https://raw.githubusercontent.com/TheBeastLT/stremio-kitsu-anime/master/static/data/imdb_mapping.json"
IDMAP_TTL = 86400       # 24 hours for individual ID mappings
FRIBB_TTL = 12 * 3600   # 12 hours for the Fribb + Kitsu indexes
_MIN_SLUG_LEN = 8       # ignore S1 slugs shorter than this to avoid false positives

# Indexes into the Fribb database
_by_anilist: dict[int, dict] = {}
_by_mal: dict[int, dict] = {}
_s1_by_tvdb: dict[int, dict] = {}       # tvdb_id -> S1 entry
_s1_by_slug: dict[str, dict] = {}       # anime-planet_id -> S1 entry
_s1_slugs_sorted: list[str] = []        # S1 slugs sorted longest-first
_kitsu_to_imdb: dict[int, str] = {}     # kitsu_id -> tt-prefixed imdb id
_fribb_loaded: float = 0


def _normalize_imdb(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return text if text.startswith("tt") else f"tt{text}"


def _extract_kitsu_imdb_map(payload) -> dict[int, str]:
    """Normalize a few plausible JSON shapes into kitsu_id -> tt-prefixed imdb."""
    mapping: dict[int, str] = {}

    def _add(kitsu_id, imdb_id) -> None:
        try:
            kid = int(kitsu_id)
        except (TypeError, ValueError):
            return
        imdb = _normalize_imdb(imdb_id)
        if imdb:
            mapping[kid] = imdb

    if isinstance(payload, list):
        for entry in payload:
            if not isinstance(entry, dict):
                continue
            _add(
                entry.get("kitsu_id", entry.get("kitsuId", entry.get("id"))),
                entry.get("imdb_id", entry.get("imdbId", entry.get("imdb"))),
            )
    elif isinstance(payload, dict):
        sample = next(iter(payload.values()), None)
        if isinstance(sample, (str, int)):
            for kitsu_id, imdb_id in payload.items():
                _add(kitsu_id, imdb_id)
        else:
            for kitsu_id, entry in payload.items():
                if isinstance(entry, dict):
                    _add(
                        entry.get("kitsu_id", entry.get("kitsuId", kitsu_id)),
                        entry.get("imdb_id", entry.get("imdbId", entry.get("imdb"))),
                    )
    return mapping


async def _ensure_fribb() -> None:
    """Load the Fribb database and Kitsu IMDb supplement if not cached or stale."""
    global _by_anilist, _by_mal, _s1_by_tvdb, _s1_by_slug, _s1_slugs_sorted, _kitsu_to_imdb, _fribb_loaded
    if _by_anilist and (time.monotonic() - _fribb_loaded) < FRIBB_TTL:
        return

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            fribb_resp = await client.get(FRIBB_URL)
            fribb_resp.raise_for_status()
            fribb_data = fribb_resp.json()

            kitsu_resp = await client.get(KITSU_IMDB_URL)
            kitsu_resp.raise_for_status()
            kitsu_data = kitsu_resp.json()
    except Exception as exc:
        logger.warning("Failed to refresh Fribb/Kitsu indexes: %s", exc)
        return

    by_anilist: dict[int, dict] = {}
    by_mal: dict[int, dict] = {}
    s1_by_tvdb: dict[int, dict] = {}
    s1_by_slug: dict[str, dict] = {}
    null_season_tv: list[dict] = []  # TV entries with season: null + tvdb_id

    for entry in fribb_data:
        aid = entry.get("anilist_id")
        if aid:
            by_anilist[aid] = entry
        mid = entry.get("mal_id")
        if mid:
            by_mal[mid] = entry
        season = entry.get("season")
        tvdb_season = (season or {}).get("tvdb")
        tvdb = entry.get("tvdb_id")
        if tvdb_season == 1:
            if tvdb:
                s1_by_tvdb[tvdb] = entry
            slug = entry.get("anime-planet_id")
            if slug and len(slug) >= _MIN_SLUG_LEN:
                s1_by_slug[slug] = entry
        elif season is None and tvdb and entry.get("type") == "TV":
            null_season_tv.append(entry)

    # Second pass: long-running TV shows (Gintama, One Piece) have season: null.
    # Treat them as S1 if no explicit season.tvdb == 1 entry claims that tvdb_id.
    for entry in null_season_tv:
        tvdb = entry["tvdb_id"]
        if tvdb not in s1_by_tvdb:
            s1_by_tvdb[tvdb] = entry
            slug = entry.get("anime-planet_id")
            if slug and len(slug) >= _MIN_SLUG_LEN:
                s1_by_slug[slug] = entry

    kitsu_to_imdb = _extract_kitsu_imdb_map(kitsu_data)

    _by_anilist = by_anilist
    _by_mal = by_mal
    _s1_by_tvdb = s1_by_tvdb
    _s1_by_slug = s1_by_slug
    _s1_slugs_sorted = sorted(s1_by_slug.keys(), key=len, reverse=True)
    _kitsu_to_imdb = kitsu_to_imdb
    _fribb_loaded = time.monotonic()
    logger.info(
        "Fribb/Kitsu loaded: %d anilist, %d mal, %d S1 tvdb, %d S1 slugs, %d kitsu imdb",
        len(by_anilist), len(by_mal), len(s1_by_tvdb), len(s1_by_slug), len(kitsu_to_imdb),
    )


def _find_entry(anilist_id: int, mal_id: int | None) -> dict | None:
    """Look up a Fribb entry by anilist_id first, then mal_id fallback."""
    return _by_anilist.get(anilist_id) or (_by_mal.get(mal_id) if mal_id else None)


def _find_s1_by_slug(entry: dict) -> dict | None:
    """Find S1 via anime-planet_id slug prefix matching."""
    slug = entry.get("anime-planet_id")
    if not slug:
        return None
    for s1_slug in _s1_slugs_sorted:
        if slug.startswith(s1_slug + "-"):
            return _s1_by_slug[s1_slug]
    return None


def _extract_imdb(entry: dict | None) -> str | None:
    """Extract a normalized tt-prefixed IMDb ID from a Fribb entry, or None."""
    if not entry:
        return None
    return _normalize_imdb(entry.get("imdb_id"))


def _maybe_kitsu_imdb(entry: dict | None) -> str | None:
    """Return a supplemental IMDb ID via Fribb kitsu_id when available."""
    if not entry:
        return None
    kitsu_id = entry.get("kitsu_id")
    try:
        return _kitsu_to_imdb.get(int(kitsu_id)) if kitsu_id is not None else None
    except (TypeError, ValueError):
        return None


def _external_id(entry: dict, fallback_anilist_id: int) -> str:
    """Pick the best external ID from a Fribb entry: IMDb > TMDB > AniList.

    If Fribb lacks imdb/tmdb for this entry, fall back to the supplemental
    Kitsu IMDb index before giving up to anilist:*.
    """
    imdb = _extract_imdb(entry) or _maybe_kitsu_imdb(entry)
    if imdb:
        return imdb
    tmdb_id = entry.get("themoviedb_id")
    if tmdb_id:
        return f"tmdb:{tmdb_id}"
    return f"anilist:{fallback_anilist_id}"


def _try_find_s1(entry: dict) -> dict | None:
    """Try to find S1 for a sequel: tvdb_id first, then slug prefix fallback."""
    tvdb_id = entry.get("tvdb_id")
    s1 = _s1_by_tvdb.get(tvdb_id) if tvdb_id else None
    if s1:
        return s1
    return _find_s1_by_slug(entry)


async def batch_map_ids(media_list: list[dict]) -> tuple[dict[int, str], dict[int, tuple[int, str]]]:
    """Map AniList IDs to TMDB/IMDb IDs via Fribb + Kitsu supplement.

    Resolution chain per entry:
    1. Fribb season.tvdb == 1 -> external ID via _external_id.
    2. Fribb season.tvdb > 1 -> trace S1 via tvdb_id or slug.
    3. Fribb null season + slug match -> sequel replacement.
    4. Remaining entries fall back to anilist:*.

    Returns (mapping, replacements):
      - mapping: anilist_id -> best external ID string
      - replacements: sequel_anilist_id -> (s1_anilist_id, s1_external_id)
    """
    await _ensure_fribb()

    mapping: dict[int, str] = {}
    replacements: dict[int, tuple[int, str]] = {}

    for media in media_list:
        anilist_id = media.get("id")
        if not anilist_id:
            continue

        cached = cache.get(f"idmap:{anilist_id}")
        if cached is not None:
            mapping[anilist_id] = cached
            cached_repl = cache.get(f"idrepl:{anilist_id}")
            if cached_repl:
                replacements[anilist_id] = cached_repl
            continue

        mal_id = media.get("idMal")
        entry = _find_entry(anilist_id, mal_id)
        tvdb_season = (entry.get("season") or {}).get("tvdb") if entry else None
        tvdb_id = entry.get("tvdb_id") if entry else None

        is_s1 = False
        if entry and tvdb_id:
            s1_entry = _s1_by_tvdb.get(tvdb_id)
            if s1_entry and s1_entry.get("anilist_id") == anilist_id:
                is_s1 = True
            elif s1_entry and s1_entry.get("mal_id") and s1_entry["mal_id"] == mal_id:
                is_s1 = True

        if is_s1 or (entry and tvdb_season == 1):
            mapped = _external_id(entry, anilist_id)
        elif entry and tvdb_season is not None and tvdb_season > 1:
            s1 = _try_find_s1(entry)
            if s1 and s1.get("anilist_id"):
                s1_aid = s1["anilist_id"]
                repl = (s1_aid, _external_id(s1, s1_aid))
                replacements[anilist_id] = repl
                cache.set(f"idrepl:{anilist_id}", repl, IDMAP_TTL)
            mapped = _external_id(entry, anilist_id)
        elif entry and entry.get("anime-planet_id"):
            s1 = _find_s1_by_slug(entry)
            if s1 and s1.get("anilist_id"):
                s1_aid = s1["anilist_id"]
                repl = (s1_aid, _external_id(s1, s1_aid))
                replacements[anilist_id] = repl
                cache.set(f"idrepl:{anilist_id}", repl, IDMAP_TTL)
            mapped = _external_id(entry, anilist_id)
        elif entry:
            mapped = _external_id(entry, anilist_id)
        else:
            mapped = f"anilist:{anilist_id}"

        mapping[anilist_id] = mapped
        if not mapped.startswith("anilist:"):
            cache.set(f"idmap:{anilist_id}", mapped, IDMAP_TTL)

    return mapping, replacements


async def reverse_lookup(external_id: str) -> int | None:
    """Given a TMDB or IMDb ID, return the AniList ID via Fribb."""
    cache_key = f"idmap_rev:{external_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    await _ensure_fribb()

    if external_id.startswith("tmdb:"):
        tmdb_num = int(external_id[5:])
        for anilist_id, entry in _by_anilist.items():
            if entry.get("themoviedb_id") == tmdb_num:
                cache.set(cache_key, anilist_id, IDMAP_TTL)
                return anilist_id
    elif external_id.startswith("tt"):
        for anilist_id, entry in _by_anilist.items():
            imdb = _extract_imdb(entry) or _maybe_kitsu_imdb(entry)
            if imdb == external_id:
                cache.set(cache_key, anilist_id, IDMAP_TTL)
                return anilist_id

    return None
