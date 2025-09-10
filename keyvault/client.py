"""Key Vault client wrapper for rotation operations."""

from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient, KeyVaultSecret
from azure.keyvault.keys import KeyClient, KeyVaultKey

from .config import vault_url_from_env


class KeyVaultClient:
    """Wrapper class for Azure Key Vault operations."""
    
    def __init__(self, vault_url: Optional[str] = None):
        self.vault_url = vault_url or vault_url_from_env()
        self.credential = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
        self.secret_client = SecretClient(vault_url=self.vault_url, credential=self.credential)
        self.key_client = KeyClient(vault_url=self.vault_url, credential=self.credential)
    
    def get_secret_status(self, secret_name: str) -> Dict[str, Any]:
        """Get the current status of a secret including versions."""
        try:
            # Get current version
            current = self.secret_client.get_secret(secret_name)
            
            # Get all versions
            versions = list(self.secret_client.list_properties_of_secret_versions(secret_name))
            versions.sort(key=lambda p: p.created_on or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
            
            version_info = []
            for i, version in enumerate(versions[:5]):  # Show last 5 versions
                tags = version.tags or {}
                version_info.append({
                    "version": version.version,
                    "created": version.created_on.isoformat() if version.created_on else "Unknown",
                    "enabled": version.enabled,
                    "is_current": i == 0,
                    "rotated_by": tags.get("rotatedBy", "Unknown"),
                    "rotation_time": tags.get("rotationTime", "Unknown")
                })
            
            return {
                "name": secret_name,
                "current_version": current.properties.version,
                "enabled": current.properties.enabled,
                "created": current.properties.created_on.isoformat() if current.properties.created_on else "Unknown",
                "updated": current.properties.updated_on.isoformat() if current.properties.updated_on else "Unknown",
                "versions": version_info,
                "total_versions": len(versions)
            }
        except Exception as e:
            return {"error": str(e), "name": secret_name}
    
    def get_key_status(self, key_name: str) -> Dict[str, Any]:
        """Get the current status of a key including versions."""
        try:
            # Get current version
            current = self.key_client.get_key(key_name)
            
            # Get all versions
            versions = list(self.key_client.list_properties_of_key_versions(key_name))
            versions.sort(key=lambda p: p.created_on or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
            
            version_info = []
            for i, version in enumerate(versions[:5]):  # Show last 5 versions
                tags = version.tags or {}
                version_info.append({
                    "version": version.version,
                    "created": version.created_on.isoformat() if version.created_on else "Unknown",
                    "enabled": version.enabled,
                    "is_current": i == 0,
                    "key_type": "Unknown",  # Key type not available in properties
                    "key_size": None
                })
            
            return {
                "name": key_name,
                "current_version": current.properties.version,
                "enabled": current.properties.enabled,
                "created": current.properties.created_on.isoformat() if current.properties.created_on else "Unknown",
                "updated": current.properties.updated_on.isoformat() if current.properties.updated_on else "Unknown",
                "key_type": current.key_type,
                "versions": version_info,
                "total_versions": len(versions)
            }
        except Exception as e:
            return {"error": str(e), "name": key_name}
    
    def get_rotation_timeline(self, secret_name: str, key_name: str) -> List[Dict[str, Any]]:
        """Get a combined timeline of secret and key rotations."""
        timeline = []
        
        try:
            # Get secret versions
            secret_versions = list(self.secret_client.list_properties_of_secret_versions(secret_name))
            for version in secret_versions:
                tags = version.tags or {}
                if version.created_on:
                    timeline.append({
                        "timestamp": version.created_on.isoformat(),
                        "type": "secret",
                        "name": secret_name,
                        "version": version.version,
                        "rotated_by": tags.get("rotatedBy", "Unknown"),
                        "enabled": version.enabled
                    })
        except Exception:
            pass  # Continue even if secret access fails
        
        try:
            # Get key versions
            key_versions = list(self.key_client.list_properties_of_key_versions(key_name))
            for version in key_versions:
                if version.created_on:
                    timeline.append({
                        "timestamp": version.created_on.isoformat(),
                        "type": "key",
                        "name": key_name,
                        "version": version.version,
                        "rotated_by": "system",  # Keys don't have custom tags
                        "enabled": version.enabled
                    })
        except Exception:
            pass  # Continue even if key access fails
        
        # Sort by timestamp descending
        timeline.sort(key=lambda x: x["timestamp"], reverse=True)
        return timeline[:20]  # Return last 20 events
