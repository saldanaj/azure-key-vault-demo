@description('Short prefix used for naming resources (keep <= 10 chars).')
param namePrefix string = 'akvdemo'

@description('Deployment location; defaults to the resource group location.')
param location string = resourceGroup().location

@description('Object ID of the deployer (AAD user or service principal) to grant Key Vault access policies.')
param deployerObjectId string

@description('Whether to create a user-assigned managed identity for future rotator/app use.')
param createUserAssignedIdentity bool = true

@description('Whether to create a Function App (Consumption) for the rotator.')
param createFunctionApp bool = true

var kvName = toLower(format('{0}-kv-{1}', namePrefix, uniqueString(resourceGroup().id)))
var uamiName = toLower(format('{0}-uami', namePrefix))

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2018-11-30' = if (createUserAssignedIdentity) {
  name: uamiName
  location: location
}

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: kvName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      name: 'standard'
      family: 'A'
    }
    enableRbacAuthorization: false
    enablePurgeProtection: false
    softDeleteRetentionInDays: 7
    accessPolicies: [
      {
        tenantId: subscription().tenantId
        objectId: deployerObjectId
        permissions: {
          keys: [
            'get'
            'list'
            'create'
            'rotate'
            'getRotationPolicy'
            'setRotationPolicy'
            'sign'
            'verify'
          ]
          secrets: [ 'get', 'list', 'set' ]
          certificates: [ 'get', 'list' ]
          storage: []
        }
      }
      if (createUserAssignedIdentity) {
        tenantId: subscription().tenantId
        objectId: uami.properties.principalId
        permissions: {
          keys: [ 'get', 'list', 'rotate', 'getRotationPolicy' ]
          secrets: [ 'get', 'list', 'set' ]
          certificates: [ 'get', 'list' ]
          storage: []
        }
      }
    ]
    enabledForDeployment: false
    enabledForDiskEncryption: false
    enabledForTemplateDeployment: false
    networkAcls: {
      bypass: 'AzureServices'
      defaultAction: 'Allow'
    }
  }
}

output keyVaultName string = kv.name
output keyVaultUri string = kv.properties.vaultUri
output userAssignedIdentityResourceId string = createUserAssignedIdentity ? uami.id : ''
output userAssignedIdentityPrincipalId string = createUserAssignedIdentity ? uami.properties.principalId : ''
output userAssignedIdentityClientId string = createUserAssignedIdentity ? uami.properties.clientId : ''

module rotatorApp 'modules/functionapp.bicep' = if (createFunctionApp && createUserAssignedIdentity) {
  name: format('{0}-rotator-func', namePrefix)
  params: {
    namePrefix: namePrefix
    location: location
    userAssignedIdentityResourceId: uami.id
    userAssignedIdentityClientId: uami.properties.clientId
    pythonVersion: '3.11'
    keyVaultUri: kv.properties.vaultUri
    secretName: 'demo-secret'
    disablePrevious: false
    keyName: 'demo-key'
    rotateKey: false
  }
}

output functionAppName string = (createFunctionApp && createUserAssignedIdentity) ? rotatorApp.outputs.functionAppName : ''
output functionAppHostname string = (createFunctionApp && createUserAssignedIdentity) ? rotatorApp.outputs.functionAppHostname : ''
