#!/usr/bin/env bash
set -euo pipefail

: "${RG:=akv-rot-demo}"
: "${APP_NAME:?Set APP_NAME to your Function App name}"

# Accept either KV_URI or KV_NAME to build KV_URI
if [[ -z "${KV_URI:-}" && -n "${KV_NAME:-}" ]]; then
  KV_URI="https://${KV_NAME}.vault.azure.net"
fi

SECRET_NAME=${SECRET_NAME:-demo-secret}
DISABLE_PREVIOUS=${DISABLE_PREVIOUS:-false}
KEY_NAME=${KEY_NAME:-demo-key}
ROTATE_KEY=${ROTATE_KEY:-false}

echo "[i] Setting app settings for $APP_NAME ..."
SETTINGS=(
  "SECRET_NAME=${SECRET_NAME}"
  "DISABLE_PREVIOUS=${DISABLE_PREVIOUS}"
  "KEY_NAME=${KEY_NAME}"
  "ROTATE_KEY=${ROTATE_KEY}"
)
if [[ -n "${KV_URI:-}" ]]; then
  SETTINGS+=("KV_URI=${KV_URI}")
fi

az functionapp config appsettings set -g "$RG" -n "$APP_NAME" --settings "${SETTINGS[@]}" -o table
echo "[✓] App settings configured."
