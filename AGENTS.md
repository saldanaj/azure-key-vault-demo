# Repository Guidelines

## Project Structure & Modules
- `infra/`: Bicep templates (`main.bicep`, `modules/`) for Key Vault, UAMI, and Function App.
- `scripts/`: Automation for deploy/seed/rotate/show/destroy (bash, idempotent where possible).
- `app/python/kv_cli/`: Minimal Python CLI to read secrets and sign with KV keys.
- `rotator/function/`: Azure Functions (Python) — timer + HTTP triggers and `shared/rotator_lib.py`.
- `.devcontainer/`: Dev container setup (Azure CLI, Bicep, Func Core Tools, Node/npm, Python venv).
- `docs/`: Overview, deploy, demo, rotator, cleanup, troubleshooting.

## Build, Test, and Development
- Dev container: “Reopen in Container” to get all tools preinstalled.
- Deploy infra: `scripts/deploy.sh <resource-group> <name-prefix> <location>`
- Seed demo data: `scripts/seed.sh` (creates secret + RSA key).
- Run CLI examples:
  - `python -m kv_cli read-secret --vault $KV_NAME --name DEMO_SECRET`
  - `python -m kv_cli sign --vault $KV_NAME --key DEMO_KEY --data "hello"`
- Publish rotator: `scripts/publish-rotator.sh`; manual rotate: `scripts/rotator-http-rotate.sh` (or `-both.sh`).
- Tear down: `scripts/destroy.sh <resource-group>`
- Tests: No formal suite yet. If adding, use `pytest`; place tests under `app/python/tests/` and `rotator/tests/`; run `pytest`.

## Coding Style & Naming
- Python: PEP 8, 4-space indent, type hints where practical. `snake_case` for functions/vars, `PascalCase` for classes. CLI entrypoint in `kv_cli/__main__.py`.
- Bicep: consistent parameter names (e.g., `namePrefix`), resource names kebab-case; avoid breaking outputs.
- Shell: POSIX-compatible; `set -euo pipefail`; file names kebab-case (e.g., `rotate-secret-now.sh`).

## Commit & Pull Request Guidelines
- Commits: Prefer Conventional Commits (`feat:`, `fix:`, `docs:`, `infra:`, `chore:`). Subject ≤ 72 chars; include concise “what/why”.
- PRs: Clear description, linked issue, testing notes (commands run, outputs), and any screenshots/logs when relevant. Keep PRs small and focused.

## Security & Configuration Tips
- Never commit secrets. Use Key Vault and environment variables (`KV_NAME` or `KV_URI`, `AZURE_CLIENT_ID`).
- Use managed identity in Azure; for local dev authenticate with `az login` (DefaultAzureCredential).
- Purge protection is disabled for demo simplicity; do not reuse for production.
