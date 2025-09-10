"""Azure Key Vault operations module for rotation demo."""

from .client import KeyVaultClient
from .rotator import rotate_secret, rotate_key_version
from .config import get_keyvault_config

__all__ = ["KeyVaultClient", "rotate_secret", "rotate_key_version", "get_keyvault_config"]
