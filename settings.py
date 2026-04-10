"""
Application settings loaded from environment variables.

All configuration is read once at import time from the .env file
(or from real environment variables in production).
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ── Server ────────────────────────────────────────────────────────────────────
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "7000"))

# ── Security ──────────────────────────────────────────────────────────────────
# Used for signing session tokens / any future server-side crypto.
# Generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY: str = os.getenv("SECRET_KEY", "")

# ── AniList OAuth ─────────────────────────────────────────────────────────────
# Required once the AniList login flow is implemented.
# Register your app at: https://anilist.co/settings/developer
ANILIST_CLIENT_ID: str = os.getenv("ANILIST_CLIENT_ID", "")
ANILIST_CLIENT_SECRET: str = os.getenv("ANILIST_CLIENT_SECRET", "")
ANILIST_REDIRECT_URI: str = os.getenv("ANILIST_REDIRECT_URI", "")

# ── OpenRouter (optional — enables AI Recommendations catalog) ────────────────
# Not required; users supply their own key via the configure UI.
# If set here it acts as a server-side fallback (future feature).
OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

# API documentation (disable by default for public deployments)
ENABLE_API_DOCS: bool = os.getenv("ENABLE_API_DOCS", "0").strip().lower() in {
    "1", "true", "yes", "on",
}
