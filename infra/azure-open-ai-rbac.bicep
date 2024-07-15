// Parameters
//////////////////////////////////////////////////
@description('The identity object/principal ID.')
param entraUserObjectId string

// Resources
//////////////////////////////////////////////////
resource openAiBuiltInAccessPolicyAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroup().id, entraUserObjectId, '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
  properties: {
    // Cognitive Services OpenAI User, from: https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles/ai-machine-learning#cognitive-services-openai-user
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')
    principalId: entraUserObjectId
    principalType: 'User'
  }
}
