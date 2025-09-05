Python CLI

Minimal CLI to interact with Azure Key Vault for the demo.

What it does
- Reads secret `demo-secret` by name and prints metadata (+ value with a flag).
- Signs a payload using key `demo-key` (RS256) and prints the `kid`.
- Optionally shows certificate metadata for `demo-cert`.

Setup
1) cd to this folder: `cd app/python`
2) Create venv and install deps:
   - `python3 -m venv .venv && source .venv/bin/activate`
   - `pip install -r requirements.txt`
3) Login to Azure: `az login` (or rely on Managed Identity when running in Azure)

Usage
- Export your Key Vault name: `export KV_NAME=<your-kv-name>`
- Read secret: `python -m kv_cli read-secret --show-value`
- Sign data: `python -m kv_cli sign --data "hello"`
- Show cert: `python -m kv_cli show-cert`

Flags
- `--vault` can accept either a KV name (e.g., `mykv`) or full URL (e.g., `https://mykv.vault.azure.net`). Defaults from `KV_NAME`.
- `--name` overrides the secret/key/cert name (defaults: `demo-secret`, `demo-key`, `demo-cert`).
