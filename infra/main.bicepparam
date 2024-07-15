using 'main.bicep'

// Injected Variables from Pipeline
//////////////////////////////////////////////////
var appenv = readEnvironmentVariable('AZURE_APPENV', '')

// Parameters
//////////////////////////////////////////////////
param location = readEnvironmentVariable('AZURE_LOCATION', '')
param currentDateTime = readEnvironmentVariable('CURRENT_DATE_TIME', '')
param openAiName = 'openai-${appenv}'
param entraUserObjectId = readEnvironmentVariable('ENTRA_USER_OBJECTID', 'bicep')
