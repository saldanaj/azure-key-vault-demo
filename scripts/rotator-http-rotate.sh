#!/usr/bin/env bash
set -euo pipefail

: "${HOST:?Set HOST to the Function App default hostname (e.g., myapp.azurewebsites.net)}"

URL="https://${HOST}/api/rotate"

echo "[i] Invoking: $URL"
curl -sS -X POST "$URL" -H 'Content-Type: application/json' -d '{}' | jq .
echo ""
