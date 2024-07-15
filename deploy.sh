#!/usr/bin/env bash

set -eo pipefail

export ENV_FILE="${1:-.env}"

export CURRENT_DATE_TIME=$(date +"%Y%m%dT%H%M")

if [ "$ENV_FILE" = ".env" ]; then
    export LOG_FILE_NAME="deploy-$CURRENT_DATE_TIME.log"
else
    SUBLOG=$(echo "$ENV_FILE" | awk -F '.' '{print $NF}')
    export LOG_FILE_NAME="$SUBLOG-deploy-$CURRENT_DATE_TIME.log"
fi

source ./logging.sh

if [ ! -f $ENV_FILE ]; then
    cp .envsample $ENV_FILE
    warn "Update $ENV_FILE with parameter values and run again"
    exit 1
fi

debug "Sourcing $ENV_FILE file"

set -a

# pulling from the .env file
source $ENV_FILE
# some other exports that are used
export AZURE_RESOURCEGROUP="rg-$AZURE_APPENV"

set +a

WORKING_DIR=$(dirname "$(realpath "$0")")
SRC_DIR="$WORKING_DIR/infra"
TEMP_DIR="$WORKING_DIR/.temp"

if [ "$ENV_FILE" != ".env" ]; then
    SUBFOLDER=$(echo "$ENV_FILE" | awk -F '.' '{print $NF}')
    TEMP_DIR="$TEMP_DIR/$SUBFOLDER"
fi

debug "Making temporary directory for merged files"
mkdir -p "$TEMP_DIR"

section "Configuring AZ CLI"

if ! az account show &> /dev/null; then
    az login
fi

info "Setting Azure subscription to $AZURE_SUBSCRIPTIONID"
az account set --subscription "$AZURE_SUBSCRIPTIONID"

info "Setting default location to $AZURE_LOCATION and resource group to $AZURE_RESOURCEGROUP"
az configure --defaults location="$AZURE_LOCATION" group="$AZURE_RESOURCEGROUP"

info "Setting Bicep to use the locally installed binary (workaround for arm64 architecture)"
az config set bicep.use_binary_from_path=True

info "Store auth token from az cli to AZURE_AUTHTOKEN"
AZURE_AUTHTOKEN=$(az account get-access-token --query 'accessToken' -o tsv)

info "Capturing current user entra details for deployment"
output=$(az ad signed-in-user show --query "{user: userPrincipalName, objectId: id}")
export ENTRA_USER_OBJECTID=$(echo "$output" | jq -r '.objectId')

section "Starting Azure infrastructure deployment"

info "Creating resource group $AZURE_RESOURCEGROUP if it does not exist"
az group create --name "$AZURE_RESOURCEGROUP" --location "$AZURE_LOCATION"

info "Transforming Bicep to ARM JSON"
START_TIME=$(date +%s)

debug "Manually building the bicep template, as there are some cross-platform issues with az deployment group create"
az bicep build --file "$SRC_DIR/main.bicep" --outdir "$TEMP_DIR"
az bicep build-params --file "$SRC_DIR/main.bicepparam" --outfile "$TEMP_DIR/main.parameters.json"

info "Initiating the Bicep deployment of infrastructure"

# TODO: use stacks instead of deployment
AZ_DEPLOYMENT_NAME="az-main-$CURRENT_DATE_TIME"
output=$(az deployment group create \
    -n "$AZ_DEPLOYMENT_NAME" \
    --template-file "$TEMP_DIR/main.json" \
    --parameters "$TEMP_DIR/main.parameters.json" \
    -g "$AZURE_RESOURCEGROUP" \
    --verbose \
    --query 'properties.outputs')

# Echo output to the log for easy access to the deployment outputs
$(echo "$output" | jq --raw-output 'to_entries[] | .value.value' | while IFS= read -r line; do debug "$line"; done)

export AZURE_OPENAI_NAME=$(echo "$output" | jq -r '.openAiName.value')
export AZURE_OPENAI_URL=$(echo "$output" | jq -r '.openAiUrl.value')

info "Deploying Open AI model $AZURE_OPENAI_MODELNAME($AZURE_OPENAI_MODELVERSION)"

envsubst < "$SRC_DIR/openai-model.json" > "$TEMP_DIR/openai-model.json"
curl -X PUT https://management.azure.com/subscriptions/$AZURE_SUBSCRIPTIONID/resourceGroups/$AZURE_RESOURCEGROUP/providers/Microsoft.CognitiveServices/accounts/$AZURE_OPENAI_NAME/deployments/$AZURE_OPENAI_MODELNAME-$AZURE_OPENAI_MODELVERSION?api-version=2023-05-01 \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $AZURE_AUTHTOKEN" \
    --data-binary "@$TEMP_DIR/openai-model.json"

END_TIME=$(date +%s)

DURATION=$((END_TIME - START_TIME))

section "Azure infrastructure deployment completed"

info "Deployment was completed in $DURATION seconds"

info "For more information, open .logs/$LOG_FILE_NAME"