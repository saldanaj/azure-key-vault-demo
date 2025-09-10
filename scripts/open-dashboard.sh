#!/usr/bin/env bash
set -euo pipefail

# Opens the local Key Vault rotation dashboard

: "${PORT:=5000}"
DASHBOARD_URL="http://localhost:${PORT}"

echo "[i] Opening local dashboard at: $DASHBOARD_URL"

# Try to open in browser
if command -v "$BROWSER" >/dev/null 2>&1; then
    "$BROWSER" "$DASHBOARD_URL"
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$DASHBOARD_URL"
elif command -v open >/dev/null 2>&1; then
    open "$DASHBOARD_URL"
else
    echo "[i] Please open this URL in your browser: $DASHBOARD_URL"
fi
