#!/usr/bin/env bash

set -eo pipefail

export ENV_FILE="${1:-.env}"

export CURRENT_DATE_TIME=$(date +"%Y%m%dT%H%M")

if [ "$ENV_FILE" = ".env" ]; then
    export LOG_FILE_NAME="remove-$CURRENT_DATE_TIME.log"
else
    SUBLOG=$(echo "$ENV_FILE" | awk -F '.' '{print $NF}')
    export LOG_FILE_NAME="$SUBLOG-remove-$CURRENT_DATE_TIME.log"
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

section "Configuring AZ CLI"

if ! az account show &> /dev/null; then
    az login
fi

info "Setting Azure subscription to $AZURE_SUBSCRIPTIONID"
az account set --subscription "$AZURE_SUBSCRIPTIONID"

info "Setting default location to $AZURE_LOCATION and resource group to $AZURE_RESOURCEGROUP"
az configure --defaults location="$AZURE_LOCATION" group="$AZURE_RESOURCEGROUP"

section "Removing Azure Infrastructure"

warn "This will remove all resources in the resource group $AZURE_RESOURCEGROUP"
warn "and any other resources created. Are you sure you want to continue? y/n"

read -r response
response=$(echo "$response" | tr '[:upper:]' '[:lower:]') # convert response to lowercase

if [[ $response == "n" || $response == "no" ]]; then
    warn "Removal cancelled. Exiting."
    exit 0
elif [[ $response == "y" || $response == "yes" ]]; then
    info "Removal confirmed, proceeding..."
else
    error "Invalid response. Exiting."
    exit 1
fi

info "Removing Resource Group"

az group delete --name "$AZURE_RESOURCEGROUP" --yes

info "Done!"
