import os
from dotenv import load_dotenv

load_dotenv()

# The application now primarily uses database-backed configuration.
# ENCRYPTION_KEY is still required for secure API key storage.
_KNOWN_WEAK_KEYS = {"default-secret-string", "your-random-secret-string"}

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY or ENCRYPTION_KEY in _KNOWN_WEAK_KEYS:
    raise RuntimeError(
        "ENCRYPTION_KEY is not set (or is a known placeholder value). "
        "Set a unique, private ENCRYPTION_KEY in your .env file before running the app.\n"
        "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    )
