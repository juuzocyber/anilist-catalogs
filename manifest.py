"""
AniList Catalogs — Stremio add-on manifest.
Defines the add-on identity and every catalog it exposes.

Catalog IDs are stable strings — changing them breaks existing installs.
"""

MANIFEST = {
    "id": "community.anilist.catalogs",
    "version": "1.4.3",
    "name": "AniList Catalogs",
    "description": (
        "Anime catalogs powered by the AniList GraphQL API. "
        "Includes Popular This Season, Airing This Week, and more."
    ),
    "logo": "https://anilist.co/img/icons/android-chrome-512x512.png",
    "background": "https://s4.anilist.co/file/anilistcdn/media/anime/banner/1-T3B0LjIARh4y.jpg",

    # Catalog for all clients; meta only for tmdb: and anilist: prefixed IDs.
    # tt* (IMDB) IDs excluded — Cinemeta serves richer meta (episodes, cast,
    # seasons) for those.  Fusion resolves tmdb: natively; regular Stremio
    # uses our meta endpoint for tmdb: and anilist: items only.
    "resources": [
        "catalog",
        {"name": "meta", "types": ["series"], "idPrefixes": ["tmdb:", "anilist:"]},
    ],

    # Stremio content types. Anime maps to "series".
    "types": ["series"],

    "catalogs": [
        {
            "type": "series",
            "id": "anilist-popular-season",
            "name": "Popular This Season",
            "extra": [
                {"name": "skip", "isRequired": False},   # pagination offset
            ],
        },
        {
            "type": "series",
            "id": "anilist-airing-week",
            "name": "Airing This Week",
            "extra": [
                {"name": "skip", "isRequired": False},
            ],
        },
        {
            "type": "series",
            "id": "anilist-trending",
            "name": "Trending Now",
            "extra": [
                {"name": "skip", "isRequired": False},
            ],
        },
        {
            "type": "series",
            "id": "anilist-top-rated",
            "name": "Top Rated All Time",
            "extra": [
                {"name": "skip", "isRequired": False},
            ],
        },
    ],

    "behaviorHints": {
        "adult": False,
        "p2pMediaFoundLinks": False,
        "configurable": False,       # will flip to True when OAuth lands
        "configurationRequired": False,
    },
}
