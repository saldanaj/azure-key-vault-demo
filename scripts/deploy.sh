#!/usr/bin/env bash
set -euo pipefail

# Config
: "${RG:=akv-rot-demo}"
: "${LOCATION:=westus2}"
: "${PREFIX:=akvdemo}"
: "${CREATE_UAMI:=true}"

echo "[i] Resource Group: $RG"
echo "[i] Location:       $LOCATION"
echo "[i] Prefix:         $PREFIX"

# Ensure Azure CLI is logged in
az account show >/dev/null 2>&1 || { echo "[!] Please run 'az login' first"; exit 1; }

# Get deployer object id (AAD)
if [[ -z "${DEPLOYER_OBJECT_ID:-}" ]]; then
  echo "[i] Resolving deployer AAD object id..."
  if ! DEPLOYER_OBJECT_ID=$(az ad signed-in-user show --query id -o tsv 2>/dev/null); then
    echo "[!] Could not resolve signed-in user via Graph. Set DEPLOYER_OBJECT_ID explicitly."
    exit 1
  fi
fi
echo "[i] Deployer Object ID: $DEPLOYER_OBJECT_ID"

echo "[i] Creating resource group if missing..."
az group create -n "$RG" -l "$LOCATION" -o none

echo "[i] Deploying Bicep (Key Vault + identity)..."
DEPLOY_OUTPUT=$(az deployment group create \
  --resource-group "$RG" \
  --template-file infra/main.bicep \
  --parameters namePrefix="$PREFIX" location="$LOCATION" deployerObjectId="$DEPLOYER_OBJECT_ID" createUserAssignedIdentity=$CREATE_UAMI \
  -o json)

if command -v jq >/dev/null 2>&1; then
  echo "$DEPLOY_OUTPUT" | jq -r '.properties.outputs | to_entries[] | "[out] \(.key)=\(.value.value)"'
else
  echo "$DEPLOY_OUTPUT" | sed -n 's/.*"keyVaultName".*"value"\s*:\s*"\([^"]*\)".*/[out] keyVaultName=\1/p'
  echo "$DEPLOY_OUTPUT" | sed -n 's/.*"keyVaultUri".*"value"\s*:\s*"\([^"]*\)".*/[out] keyVaultUri=\1/p'
  echo "$DEPLOY_OUTPUT" | sed -n 's/.*"userAssignedIdentityResourceId".*"value"\s*:\s*"\([^"]*\)".*/[out] userAssignedIdentityResourceId=\1/p'
  echo "$DEPLOY_OUTPUT" | sed -n 's/.*"userAssignedIdentityPrincipalId".*"value"\s*:\s*"\([^"]*\)".*/[out] userAssignedIdentityPrincipalId=\1/p'
  echo "$DEPLOY_OUTPUT" | sed -n 's/.*"userAssignedIdentityClientId".*"value"\s*:\s*"\([^"]*\)".*/[out] userAssignedIdentityClientId=\1/p'
fi

echo "[✓] Deployment complete. See outputs above for the Key Vault name/URI."
