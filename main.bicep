param location string = resourceGroup().location
param existingStorageName string = 'todostorageassignment'
param repoUrl string = 'https://github.com/MaximusAnakin/todo'
param repoBranch string = 'main'

var functionAppName = 'todo-backend-func'
var staticWebAppName = 'todo-frontend'
var planName = '${functionAppName}-plan'

resource storage 'Microsoft.Storage/storageAccounts@2022-09-01' existing = {
  name: existingStorageName
}

resource plan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: planName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  kind: 'Linux'
  properties: {
    reserved: true
  }
}

resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: functionAppName
  location: location
  kind: 'functionapp,linux'
  properties: {
    serverFarmId: plan.id
    siteConfig: {
      appSettings: [
        { name: 'FUNCTIONS_WORKER_RUNTIME', value: 'python' }
        { name: 'PYTHON_VERSION', value: '3.11' }
        { name: 'FUNCTIONS_EXTENSION_VERSION', value: '~4' }
        { name: 'AzureWebJobsStorage', value: storage.properties.primaryEndpoints.blob }
      ]
    }
  }
}

resource staticWebApp 'Microsoft.Web/staticSites@2022-03-01' = {
  name: staticWebAppName
  location: location
  sku: {
    name: 'Free'
    tier: 'Free'
}
  properties: {
    repositoryUrl: repoUrl
    branch: repoBranch
    buildProperties: {
      appLocation: 'frontend'
      apiLocation: 'backend'
    }
  }
}
