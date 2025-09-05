Run the Demo

Note: In the dev container, activate the Python venv first from repo root: `source .venv/bin/activate`.

1) Seed initial assets
- `scripts/seed.sh` creates:
  - Secret `demo-secret` with a timestamped value
  - RSA key `demo-key` (2048)

2) Baseline read
- `scripts/show-versions.sh` shows current versions.
- Python CLI:
  - `cd app/python && python -m kv_cli read-secret --vault "$KV_NAME" --show-value`
  - `cd app/python && python -m kv_cli sign --vault "$KV_NAME" --data "hello"`

3) Rotate and observe
- Secret rotation (manual): `scripts/rotate-secret-now.sh`
  - Re-run `show-versions.sh` and the CLI to see the new secret version picked up.
- Key rotation (manual): `scripts/rotate-key-now.sh`
  - Re-run the CLI; the `kid` changes, demonstrating a new key version.
 - HTTP rotator (manual, secret only or secret+key):
   - Secret only: `HOST=<functionAppHostname> scripts/rotator-http-rotate.sh`
   - Secret + key: `HOST=<functionAppHostname> scripts/rotator-http-rotate-both.sh`

4) Cleanup
- `scripts/destroy.sh`

Notes
- Timer function rotates the secret every 5 minutes; use the HTTP endpoint to manually rotate at demo time.
