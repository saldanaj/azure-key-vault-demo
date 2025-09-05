#!/usr/bin/env bash
set -euo pipefail

: "${RG:=akv-rot-demo}"

echo "[i] Deleting resource group '$RG'..."
az group delete -n "$RG" --yes --no-wait
echo "[✓] Delete requested. Resources will be removed asynchronously."
