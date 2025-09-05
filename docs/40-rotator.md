Rotator Function

What it does
- Timer trigger (every 5 minutes) creates a new version of `SECRET_NAME` in Key Vault and tags it with metadata.
- HTTP endpoint `/api/rotate` creates a new version on demand for demo purposes.
- Optional: disables the previous secret version if `DISABLE_PREVIOUS=true`.

App settings
- `KV_URI`: Full Key Vault URI, e.g., `https://<kv>.vault.azure.net` (or set `KV_NAME` instead).
- `SECRET_NAME`: Secret to rotate (default `demo-secret`).
- `DISABLE_PREVIOUS`: `true`/`false` (default `false`).

Configure settings
- `RG=akv-rot-demo APP_NAME=<function-app-name> KV_NAME=<kv-name> SECRET_NAME=demo-secret DISABLE_PREVIOUS=false scripts/config-rotator.sh`

Publish function code
- Requires Azure Functions Core Tools v4.
- `APP_NAME=<function-app-name> scripts/publish-rotator.sh`

Local development
- In the dev container, activate the Python venv from repo root first: `source .venv/bin/activate`.
- From `rotator/function`, run: `func start` (ensure `KV_URI`/`KV_NAME` env vars are set in your shell for local run).

Trigger HTTP rotate
- Find the hostname from deployment output (`functionAppHostname`).
- Rotate secret only: `HOST=<functionAppHostname> scripts/rotator-http-rotate.sh`
- Rotate secret + key: `HOST=<functionAppHostname> scripts/rotator-http-rotate-both.sh`

Manual control
- Key rotation is manual by default: timer does not rotate the key.
- The HTTP endpoint accepts `?rotateKey=true` to rotate both in one call. You can also set app setting `ROTATE_KEY=true` to make the HTTP default include key rotation, but we recommend leaving it `false` and using the query parameter during the demo.

Verify
- `KV_NAME=<kv> scripts/show-versions.sh`
- Run the Python CLI again to see the new secret version picked up.
