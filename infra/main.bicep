// Parameters
param location string = resourceGroup().location
param currentDateTime string
param entraUserObjectId string
param openAiName string

resource openAi 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAiName
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: toLower(openAiName)
    disableLocalAuth: true
  }
}

module openAiRbac './azure-open-ai-rbac.bicep' = {
  name: 'az-openai-rbac-${currentDateTime}'
  dependsOn: [
    openAi
  ]
  params: {
    entraUserObjectId: entraUserObjectId
  }
}

output openAiName string = openAi.name
output openAiUrl string = openAi.properties.endpoint
