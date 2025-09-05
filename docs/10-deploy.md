Deploy

Prerequisites
- Use the repo’s dev container OR have locally: Azure CLI (with Bicep), Azure Functions Core Tools v4, Python 3.11, jq.
- Logged in with `az login` and the right subscription selected.
- Permissions to create resource groups and Key Vault.

Quick start
1) Set environment variables (adjust as needed):
   - `export RG=akv-rot-demo`
   - `export LOCATION=eastus`
   - `export PREFIX=akvdemo`

2) Deploy infra (resource group, Key Vault, user-assigned identity, Function App Consumption):
   - `scripts/deploy.sh`

3) Capture outputs (Key Vault name/URI, Function App name/hostname, UAMI IDs).

Notes
- The template uses access policies and grants the deployer full access for demo purposes.
- Keep `PREFIX` short (<=10) to satisfy Key Vault name length limits.
- A Linux Consumption Function App and Storage Account are created for the rotator (no code deployed yet).
