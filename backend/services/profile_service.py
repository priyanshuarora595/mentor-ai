import os
import hashlib
import base64
from cryptography.fernet import Fernet
from database.db import SessionLocal, engine
from database.models import ModelConfig, Base
from dotenv import load_dotenv

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

load_dotenv()

# Centralized defaults (replaces environment variables)
DEFAULT_CONFIG = {"provider": "ollama", "model": "llama3", "api_key": ""}


def derive_fernet_key(key_string: str) -> bytes:
    """
    Derives a 32-byte URL-safe base64-encoded key from an arbitrary string.
    This allows any random string to provide a valid Fernet key.
    """
    if not key_string:
        return Fernet.generate_key()

    # Use SHA-256 to hash the input string to exactly 32 bytes
    hash_obj = hashlib.sha256(key_string.encode())
    key_32bytes = hash_obj.digest()

    # Base64 encode the 32 bytes to make it Fernet-compatible
    return base64.urlsafe_b64encode(key_32bytes)


# Encryption setup
raw_key = os.getenv("ENCRYPTION_KEY", "default-secret-string")
ENCRYPTION_KEY = derive_fernet_key(raw_key)
fernet = Fernet(ENCRYPTION_KEY)


def encrypt_key(api_key):
    if not api_key:
        return ""
    return fernet.encrypt(api_key.encode()).decode()


def decrypt_key(encrypted_key):
    if not encrypted_key:
        return ""
    try:
        return fernet.decrypt(encrypted_key.encode()).decode()
    except Exception:
        return ""


def load_profile(user_id=1):
    db = SessionLocal()
    try:
        config = db.query(ModelConfig).filter(ModelConfig.user_id == user_id).first()
        if not config:
            return {"model_config": DEFAULT_CONFIG.copy()}

        return {
            "model_config": {
                "provider": config.provider,
                "model": config.model_name,
                "api_key": decrypt_key(config.api_key),
            }
        }
    finally:
        db.close()


def save_profile(profile, user_id=1):
    db = SessionLocal()
    try:
        model_config = profile.get("model_config", {})
        config = db.query(ModelConfig).filter(ModelConfig.user_id == user_id).first()

        provider = model_config.get("provider", DEFAULT_CONFIG["provider"])
        model_name = model_config.get("model", DEFAULT_CONFIG["model"])
        api_key = encrypt_key(model_config.get("api_key", ""))

        if config:
            config.provider = provider
            config.model_name = model_name
            config.api_key = api_key
        else:
            new_config = ModelConfig(
                user_id=user_id,
                provider=provider,
                model_name=model_name,
                api_key=api_key,
            )
            db.add(new_config)

        db.commit()
    finally:
        db.close()
