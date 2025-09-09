#!/usr/bin/env bash
set -euo pipefail

: "${KV_NAME:?Set KV_NAME to your Key Vault name}"
SECRET_NAME=${SECRET_NAME:-demo-secret}
KEY_NAME=${KEY_NAME:-demo-key}

echo "[i] Key Vault: $KV_NAME"

echo "\n[>] Secret versions: $SECRET_NAME"
az keyvault secret list-versions --vault-name "$KV_NAME" -n "$SECRET_NAME" -o table || echo "(none)"

echo "\n[>] Key versions: $KEY_NAME"
az keyvault key list-versions --vault-name "$KV_NAME" -n "$KEY_NAME" -o table || echo "(none)"
