"""
Simple in-memory TTL cache.

Each entry stores the value and the time it was written.
On read, if (now - written_at) > ttl the entry is treated as missing.

Thread-safe enough for a single-process FastAPI/uvicorn deployment.
Swap this out for Redis when you move to multi-worker hosting.
"""

import time
from typing import Any, Optional


class TTLCache:
    def __init__(self) -> None:
        self._store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if time.monotonic() > expires_at:
            del self._store[key]
            return None
        return value

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        self._store[key] = (value, time.monotonic() + ttl_seconds)

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def __len__(self) -> int:
        return len(self._store)


# Singleton used across the app
cache = TTLCache()

# TTLs per catalog (seconds)
TTL = {
    "anilist-popular-season": 15 * 60,   # 15 minutes
    "anilist-airing-week":    60 * 60,   # 1 hour
    "anilist-trending":       15 * 60,   # 15 minutes
    "anilist-top-rated":      6 * 60 * 60,  # 6 hours (changes slowly)
    "meta":                   30 * 60,   # 30 minutes
}
