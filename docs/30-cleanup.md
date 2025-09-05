Cleanup

- Delete everything by deleting the resource group:
  - `scripts/destroy.sh`

Validate
- Ensure the resource group no longer appears in `az group list`.
- Key Vault purge protection is disabled in this demo to allow clean deletion.

