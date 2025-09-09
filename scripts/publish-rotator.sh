#!/usr/bin/env bash
set -euo pipefail

# Publishes the rotator Function App using Azure Functions Core Tools (func)

: "${APP_NAME:?Set APP_NAME to your Function App name (output from deploy)}"

if ! command -v func >/dev/null 2>&1; then
  echo "[!] Azure Functions Core Tools (func) not found. Install v4: https://aka.ms/azfunc-install"
  exit 1
fi

pushd rotator/function >/dev/null
echo "[i] Publishing to Function App: $APP_NAME"
func azure functionapp publish "$APP_NAME" --python
popd >/dev/null

echo "[✓] Publish complete."
