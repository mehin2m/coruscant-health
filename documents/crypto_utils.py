"""
File-level encryption for uploaded documents (AES-128 via Fernet, which is
the cryptography library's authenticated-encryption recipe built on AES-CBC
+ HMAC). The key must come from the environment, never be hard-coded, and
never be committed to source control.
"""
import os
from cryptography.fernet import Fernet
from django.core.exceptions import ImproperlyConfigured


def get_fernet() -> Fernet:
    key = os.environ.get("DOCUMENT_ENCRYPTION_KEY")
    if not key:
        raise ImproperlyConfigured(
            "DOCUMENT_ENCRYPTION_KEY environment variable is not set. "
            "Generate one with Fernet.generate_key() and store it as a secret."
        )
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_bytes(data: bytes) -> bytes:
    return get_fernet().encrypt(data)


def decrypt_bytes(token: bytes) -> bytes:
    return get_fernet().decrypt(token)
