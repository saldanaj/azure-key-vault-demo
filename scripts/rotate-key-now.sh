#!/usr/bin/env bash
set -euo pipefail

: "${KV_NAME:?Set KV_NAME to your Key Vault name}"
KEY_NAME=${KEY_NAME:-demo-key}

echo "[i] Rotating key '$KEY_NAME'..."
az keyvault key rotate --vault-name "$KV_NAME" --name "$KEY_NAME" -o json | sed -n "s/.*\"kid\".*\"\(.*\)\".*/[out] kid=\1/p"
echo "[✓] Key rotated."
