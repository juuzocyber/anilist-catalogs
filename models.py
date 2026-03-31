"""
Pydantic models that match Stremio's catalog and meta response shapes.
Reference: https://github.com/Stremio/stremio-addon-sdk/blob/master/docs/api/responses/meta.md
"""

from typing import Optional
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Stremio Meta object (used in both catalog previews and full meta responses)
# ---------------------------------------------------------------------------

class MetaPreview(BaseModel):
    """Lightweight meta used inside catalog responses."""
    id: str           # e.g. "anilist:12345"
    type: str         # always "series" for anime
    name: str
    poster: Optional[str] = None
    posterShape: str = "poster"   # "poster" | "landscape" | "square"
    background: Optional[str] = None
    description: Optional[str] = None
    releaseInfo: Optional[str] = None   # e.g. "2024" or "2024-2025"
    imdbRating: Optional[str] = None    # AniList score mapped here (display only)
    genres: Optional[list[str]] = None


class MetaDetail(MetaPreview):
    """Full meta object returned by /meta endpoint."""
    website: Optional[str] = None
    trailers: Optional[list[dict]] = None
    links: Optional[list[dict]] = None
    behaviorHints: Optional[dict] = None


# ---------------------------------------------------------------------------
# Stremio response wrappers
# ---------------------------------------------------------------------------

class CatalogResponse(BaseModel):
    metas: list[MetaPreview]


class MetaResponse(BaseModel):
    meta: MetaDetail
