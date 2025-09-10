"""Key and secret rotation functions."""

import random
import string
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient

from .config import vault_url_from_env


def _generate_value(n: int = 24) -> str:
    """Generate a random value for secret rotation."""
    alphabet = string.ascii_letters + string.digits
    return "rot-" + "".join(random.choice(alphabet) for _ in range(n))


def _credential():
    """Get Azure credentials."""
    return DefaultAzureCredential(exclude_shared_token_cache_credential=True)


def rotate_secret(
    secret_name: str,
    rotated_by: str = "manual",
    provided_value: Optional[str] = None,
    disable_previous: bool = False
) -> Dict[str, Any]:
    """
    Rotate a Key Vault secret.
    
    Args:
        secret_name: Name of the secret to rotate
        rotated_by: Who/what initiated the rotation
        provided_value: Specific value to use (if None, generates random value)
        disable_previous: Whether to disable the previous version
    
    Returns:
        Dictionary with rotation results
    """
    kv_url = vault_url_from_env()
    cred = _credential()
    client = SecretClient(vault_url=kv_url, credential=cred)

    value = provided_value or _generate_value()
    tags = {
        "rotatedBy": rotated_by,
        "rotationTime": datetime.now(timezone.utc).isoformat(),
    }
    new = client.set_secret(secret_name, value, tags=tags)

    previous_version = None
    disabled_previous = False

    if disable_previous:
        versions = list(client.list_properties_of_secret_versions(secret_name))
        # Sort descending by created_on and pick the first version different from new
        versions.sort(key=lambda p: p.created_on or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        for p in versions:
            if p.version != new.properties.version:
                previous_version = p.version
                if p.enabled:
                    client.update_secret_properties(secret_name, p.version, enabled=False)
                    disabled_previous = True
                break

    return {
        "secret_name": secret_name,
        "new_version": new.properties.version,
        "previous_version": previous_version,
        "disabled_previous": disabled_previous,
        "kv_url": kv_url,
        "rotated_by": rotated_by,
        "rotation_time": tags["rotationTime"]
    }


def rotate_key_version(key_name: str, rotated_by: str = "manual") -> Dict[str, Any]:
    """
    Rotate a Key Vault key.
    
    Args:
        key_name: Name of the key to rotate
        rotated_by: Who/what initiated the rotation
    
    Returns:
        Dictionary with rotation results
    """
    kv_url = vault_url_from_env()
    cred = _credential()
    client = KeyClient(vault_url=kv_url, credential=cred)
    new_key = client.rotate_key(key_name)
    
    return {
        "key_name": key_name,
        "key_kid": new_key.id,
        "new_version": new_key.properties.version,
        "kv_url": kv_url,
        "rotated_by": rotated_by,
        "rotation_time": datetime.now(timezone.utc).isoformat()
    }
