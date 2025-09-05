Troubleshooting

- Access denied (403) when reading secrets/keys
  - Ensure your AAD object id was passed as `deployerObjectId` and appears in Key Vault access policies.
  - Re-run deploy with the correct object id: `az ad signed-in-user show --query id -o tsv`.

- Key Vault name conflicts
  - Use a different `PREFIX`; KV name is derived from prefix + unique string, must be <= 24 chars.

- Destroy fails due to purge protection
  - This template disables purge protection. If tenant policy forces it, deletion may require purge steps or waiting for retention.

- CLI cannot sign using key
  - The deployer needs key crypto permissions (sign/verify). Redeploy or add an access policy entry.

