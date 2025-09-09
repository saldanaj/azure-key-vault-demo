#!/usr/bin/env bash
set -euo pipefail

: "${KV_NAME:?Set KV_NAME to your Key Vault name}"
SECRET_NAME=${SECRET_NAME:-demo-secret}

NEW_VALUE=${NEW_VALUE:-"demo-$(date +%s)"}
echo "[i] Creating new secret version for '$SECRET_NAME'..."
az keyvault secret set --vault-name "$KV_NAME" --name "$SECRET_NAME" --value "$NEW_VALUE" -o jsonc | sed -n "s/.*\"id\".*\"\(.*\)\".*/[out] id=\1/p;s/.*\"kid\".*\"\(.*\)\".*/[out] kid=\1/p;s/.*\"version\".*\"\(.*\)\".*/[out] version=\1/p"
echo "[✓] Secret rotated."
