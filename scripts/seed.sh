#!/usr/bin/env bash
set -euo pipefail

: "${KV_NAME:?Set KV_NAME to your Key Vault name}"

SECRET_NAME=${SECRET_NAME:-demo-secret}
KEY_NAME=${KEY_NAME:-demo-key}

echo "[i] Seeding secret '$SECRET_NAME'..."
az keyvault secret set --vault-name "$KV_NAME" --name "$SECRET_NAME" --value "demo-$(date +%s)" -o none

echo "[i] Creating RSA key '$KEY_NAME' (2048)..."
az keyvault key create --vault-name "$KV_NAME" --name "$KEY_NAME" --kty RSA --size 2048 -o none

echo "[✓] Seed complete."
