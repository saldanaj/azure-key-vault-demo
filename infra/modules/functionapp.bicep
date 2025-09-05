@description('Short prefix for naming resources (<= 10 chars).')
param namePrefix string

@description('Location for all resources.')
param location string

@description('Resource ID of an existing User Assigned Managed Identity to attach to the Function App.')
param userAssignedIdentityResourceId string

@description('Client ID of the User Assigned Managed Identity (used for AZURE_CLIENT_ID).')
param userAssignedIdentityClientId string

@description('Function App name (optional). If empty, a name will be generated.')
@minLength(0)
param functionAppName string = ''

@description('Runtime Python version for the Function App.')
param pythonVersion string = '3.11'

@description('Key Vault URI to pass as app setting (KV_URI). Optional.')
@minLength(0)
param keyVaultUri string = ''

@description('Default secret name to rotate (SECRET_NAME).')
param secretName string = 'demo-secret'

@description('Disable previous secret version after rotation (DISABLE_PREVIOUS).')
param disablePrevious bool = false

@description('Default key name for manual rotation (KEY_NAME).')
param keyName string = 'demo-key'

@description('Rotate key by default on HTTP call if not overridden (ROTATE_KEY).')
param rotateKey bool = false

var saName = toLower(replace(format('{0}st{1}', namePrefix, uniqueString(resourceGroup().id)), '-', ''))
var planName = toLower(format('{0}-plan', namePrefix))
var siteName = empty(functionAppName) ? toLower(format('{0}-func', namePrefix)) : toLower(functionAppName)

resource sa 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: saName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
  }
}

@description('Get primary storage key for Function App settings')
var saKey = listKeys(sa.id, sa.apiVersion).keys[0].value

var saConn = format('DefaultEndpointsProtocol=https;AccountName={0};AccountKey={1};EndpointSuffix={2}', sa.name, saKey, environment().suffixes.storage)

resource plan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: planName
  location: location
  kind: 'functionapp'
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
    size: 'Y1'
    family: 'Y'
    capacity: 0
  }
  properties: {
    reserved: true // Linux
  }
}

resource app 'Microsoft.Web/sites@2023-01-01' = {
  name: siteName
  location: location
  kind: 'functionapp,linux'
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${userAssignedIdentityResourceId}': {}
    }
  }
  properties: {
    httpsOnly: true
    serverFarmId: plan.id
    siteConfig: {
      linuxFxVersion: format('PYTHON|{0}', pythonVersion)
      minimumTlsVersion: '1.2'
      http20Enabled: true
      appSettings: [
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'AzureWebJobsStorage'
          value: saConn
        }
        {
          name: 'WEBSITE_RUN_FROM_PACKAGE'
          value: '1'
        }
        {
          name: 'AZURE_CLIENT_ID'
          value: userAssignedIdentityClientId
        }
        if (!empty(keyVaultUri)) {
          name: 'KV_URI'
          value: keyVaultUri
        }
        {
          name: 'SECRET_NAME'
          value: secretName
        }
        {
          name: 'DISABLE_PREVIOUS'
          value: string(disablePrevious)
        }
        {
          name: 'KEY_NAME'
          value: keyName
        }
        {
          name: 'ROTATE_KEY'
          value: string(rotateKey)
        }
      ]
    }
  }
}

output functionAppName string = app.name
output functionAppHostname string = app.properties.defaultHostName
output storageAccountName string = sa.name
