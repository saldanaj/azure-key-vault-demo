# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

This is an Azure Key Vault rotation demo with three main components:
- **Infrastructure** (`infra/`): Bicep templates for Azure resources (Key Vault, Function App, managed identity)
- **Python CLI** (`app/python/`): Command-line tool for reading secrets, signing data, and showing certificates
- **Rotator Function** (`rotator/function/`): Azure Function App with timer and HTTP triggers for secret/key rotation

## Common Commands

### Development Setup
```bash
# In dev container (recommended)
source .venv/bin/activate

# Local setup (if not using dev container)
cd app/python && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

### Infrastructure Deployment
```bash
# Deploy infrastructure
RG=akv-rot-demo LOCATION=eastus PREFIX=akvdemo scripts/deploy.sh

# Seed initial secrets/keys
KV_NAME=<from-deploy-output> scripts/seed.sh

# Clean up resources
RG=akv-rot-demo scripts/destroy.sh
```

### Running the CLI
The Python CLI (`kv_cli`) operates on Key Vault resources by name (no version) to demonstrate natural rotation pickup:

```bash
# Read secret metadata and value
python -m kv_cli read-secret --vault "$KV_NAME" --show-value

# Sign data using Key Vault key
python -m kv_cli sign --vault "$KV_NAME" --data "hello"

# Show certificate info
python -m kv_cli show-cert --vault "$KV_NAME"
```

### Rotation Operations
```bash
# Rotate secret only
KV_NAME=$KV_NAME scripts/rotate-secret-now.sh

# Rotate key only  
KV_NAME=$KV_NAME scripts/rotate-key-now.sh

# HTTP-triggered rotation (requires deployed Function App)
HOST=<functionAppHostname> scripts/rotator-http-rotate.sh          # secret only
HOST=<functionAppHostname> scripts/rotator-http-rotate-both.sh     # secret + key
```

### Function App Management
```bash
# Publish rotator function
scripts/publish-rotator.sh

# Configure rotator settings
scripts/config-rotator.sh

# Show asset versions
scripts/show-versions.sh
```

## Architecture Notes

### Authentication Flow
- Uses `DefaultAzureCredential` for both local development (`az login`) and Azure deployment (managed identity)
- Key Vault access policies grant deployer and managed identity appropriate permissions
- No version-specific references in client code - always gets latest version

### Key Vault Integration
- Secret client: Read metadata, get values, set new versions
- Key client: Get keys, rotate keys, cryptographic operations (signing)
- Certificate client: Read certificate metadata and properties
- All clients use vault name/URL resolution via `_vault_url_from_name()`

### Function App Structure
- Timer trigger (`RotatorTimer`): Scheduled secret rotation
- HTTP trigger (`RotateNow`): On-demand rotation with optional key rotation
- Shared library (`shared/rotator_lib.py`): Core rotation logic for secrets and keys
- Environment variables: `KV_URI`/`KV_NAME`, `SECRET_NAME`, `KEY_NAME`

### Infrastructure as Code
- Main template (`infra/main.bicep`): Key Vault + managed identity + Function App module
- Function App module (`infra/modules/functionapp.bicep`): Consumption plan with managed identity
- Access policies over RBAC for simplified demo setup
- Short retention (7 days) and disabled purge protection for easy cleanup