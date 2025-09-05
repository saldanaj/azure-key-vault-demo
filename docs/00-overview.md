Overview

This demo shows how secret and key rotation in Azure Key Vault results in new versions that applications transparently consume when they read by name (not by version).

What you’ll see
- Key Vault with one secret and one RSA key.
- A simple Python CLI that reads the secret, and signs a payload using the key (showing the key ID changes across rotations).
- Manual rotation (scripts) and an automated rotator (Azure Functions on the Consumption plan) for secrets; optional HTTP-initiated key rotation.

Scope
- Primary: Secret rotation (new version) and Key rotation (new key version / new kid).
- Optional: Certificate scenario (self-signed, short lifetime, auto-renew) can be added if needed.

Principles
- Minimal cost: Standard Key Vault, Functions Consumption plan, Standard_LRS storage, single resource group, easy tear-down.
- No embedded creds: Use Azure AD auth (`DefaultAzureCredential`) and access policies.
- Disposable: One-line deploy and one-line destroy.

Next steps
- Develop in the provided dev container (installs az, bicep, func, node, jq).
- Deploy infra: Key Vault + managed identity + Function App.
- Seed initial key/secret.
- Run the CLI to show baseline values.
- Rotate and observe changes.
