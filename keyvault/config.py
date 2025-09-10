"""Configuration management for Key Vault operations."""

import os
from typing import Dict, Any


def get_keyvault_config() -> Dict[str, Any]:
    """Get Key Vault configuration from environment variables."""
    kv_uri = os.getenv("KV_URI")
    kv_name = os.getenv("KV_NAME")
    
    if kv_uri:
        vault_url = kv_uri.rstrip('/')
        # Extract name from URI if not provided
        if not kv_name:
            kv_name = kv_uri.replace("https://", "").replace("http://", "").split(".")[0]
    elif kv_name:
        vault_url = f"https://{kv_name}.vault.azure.net"
    else:
        raise RuntimeError("KV_URI or KV_NAME must be set in environment variables.")
    
    return {
        "vault_url": vault_url,
        "vault_name": kv_name,
        "secret_name": os.getenv("SECRET_NAME", "demo-secret"),
        "key_name": os.getenv("KEY_NAME", "demo-key"),
    }


def vault_url_from_env() -> str:
    """Get the Key Vault URL from environment variables."""
    return get_keyvault_config()["vault_url"]
