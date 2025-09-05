import os
import random
import string
from datetime import datetime, timezone
from typing import Optional, Tuple

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient


def _vault_url_from_env() -> str:
    kv_uri = os.getenv("KV_URI")
    kv_name = os.getenv("KV_NAME")
    if kv_uri:
        return kv_uri.rstrip('/')
    if kv_name:
        return f"https://{kv_name}.vault.azure.net"
    raise RuntimeError("KV_URI or KV_NAME must be set in app settings.")


def _credential():
    return DefaultAzureCredential(exclude_shared_token_cache_credential=True)


def _generate_value(n: int = 24) -> str:
    alphabet = string.ascii_letters + string.digits
    return "rot-" + "".join(random.choice(alphabet) for _ in range(n))


def rotate_secret(rotated_by: str = "timer", provided_value: Optional[str] = None, disable_previous: bool = False) -> dict:
    secret_name = os.getenv("SECRET_NAME", "demo-secret")
    kv_url = _vault_url_from_env()
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
    }


def rotate_key_version(rotated_by: str = "http") -> dict:
    key_name = os.getenv("KEY_NAME", "demo-key")
    kv_url = _vault_url_from_env()
    cred = _credential()
    client = KeyClient(vault_url=kv_url, credential=cred)
    new_key = client.rotate_key(key_name)
    return {
        "key_name": key_name,
        "key_kid": new_key.id,
        "kv_url": kv_url,
    }
