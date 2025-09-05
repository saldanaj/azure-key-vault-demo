#!/usr/bin/env bash
set -euo pipefail

echo "[devcontainer] Installing jq and prerequisites..."
sudo apt-get update -y >/dev/null
sudo apt-get install -y jq >/dev/null

echo "[devcontainer] Ensuring Bicep is installed via Azure CLI..."
az bicep install || true

echo "[devcontainer] Installing Azure Functions Core Tools v4..."
npm i -g azure-functions-core-tools@4 --unsafe-perm true >/dev/null 2>&1 || {
  echo "[warn] Failed to install func core tools via npm. You can install manually later.";
}

echo "[devcontainer] Creating Python venv and installing requirements..."
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
pip install -r app/python/requirements.txt >/dev/null || echo "[warn] Failed to install app/python requirements"
pip install -r rotator/function/requirements.txt >/dev/null || echo "[warn] Failed to install rotator/function requirements"
deactivate || true

echo "[devcontainer] Node and npm installed via devcontainer feature."

echo "[devcontainer] Done."
