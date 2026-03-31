"""
AniList Catalogs — symmetric encryption helpers.

Provides encrypt/decrypt for strings using Fernet (AES-128-CBC + HMAC-SHA256).
The Fernet key is derived from SECRET_KEY via SHA-256 so any arbitrary string
can be used as the source secret.

Typical use: encrypt AniList access tokens before embedding them in config URLs.
"""

import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken

from settings import SECRET_KEY


def _derive_key(secret: str) -> bytes:
    """Return a 32-byte URL-safe base64 key derived from *secret* via SHA-256."""
    digest = hashlib.sha256(secret.encode()).digest()  # always 32 bytes
    return base64.urlsafe_b64encode(digest)


def _fernet() -> Fernet:
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is not set. Add it to .env before using encryption."
        )
    return Fernet(_derive_key(SECRET_KEY))


def encrypt(plaintext: str) -> str:
    """Encrypt *plaintext* and return a URL-safe base64 token string."""
    return _fernet().encrypt(plaintext.encode()).decode()


def decrypt(token: str) -> str:
    """Decrypt a token produced by :func:`encrypt` and return the original string.

    Raises :class:`cryptography.fernet.InvalidToken` if the token is invalid,
    tampered with, or was encrypted with a different key.
    """
    return _fernet().decrypt(token.encode()).decode()
