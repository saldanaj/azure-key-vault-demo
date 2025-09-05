Rotator Function

What it does
- Timer trigger (`0 */5 * * * *`) rotates the secret (creates new version with tags).
- HTTP trigger `/api/rotate` rotates the secret on demand; add `?rotateKey=true` to also rotate the key.

Auth
- Uses User-Assigned Managed Identity + Key Vault access policies.
  - Secrets: set/get/list/update
  - Keys: get/list/rotate (for optional key rotation)

Configuration
- App settings:
  - `KV_URI` (or `KV_NAME`): Key Vault to target.
  - `SECRET_NAME`: Secret to rotate (default `demo-secret`).
  - `DISABLE_PREVIOUS`: If `true`, disables the prior version after creating a new one.
  - `KEY_NAME`: Key to rotate manually via HTTP (default `demo-key`).
  - `ROTATE_KEY`: Default behavior for HTTP (leave `false`; prefer `?rotateKey=true`).

Local development
- Functions Core Tools v4 is installed in the dev container.
- From `rotator/function`: `func start` (requires local app settings or env vars for KV).
