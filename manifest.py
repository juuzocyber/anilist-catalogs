"""
AniList Catalogs — Stremio add-on manifest.
Defines the add-on identity and every catalog it exposes.

Catalog IDs are stable strings — changing them breaks existing installs.
"""

MANIFEST = {
    "id": "community.anilist.catalogs",
    "version": "0.1.0",
    "name": "AniList Catalogs",
    "description": (
        "Anime catalogs powered by the AniList GraphQL API. "
        "Includes Popular This Season, Airing This Week, and more."
    ),
    "logo": "https://anilist.co/img/icons/android-chrome-512x512.png",
    "background": "https://s4.anilist.co/file/anilistcdn/media/anime/banner/1-T3B0LjIARh4y.jpg",

    # We only serve catalog + meta — no streams.
    "resources": ["catalog", "meta"],

    # Stremio content types. Anime maps to "series".
    "types": ["series"],

    "idPrefixes": ["anilist:"],

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
