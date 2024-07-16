#!/usr/bin/env bash

set -eo pipefail

export ENV_FILE="${1:-.env}"

export CURRENT_DATE_TIME=$(date +"%Y%m%dT%H%M")

if [ "$ENV_FILE" = ".env" ]; then
    export LOG_FILE_NAME="run-$CURRENT_DATE_TIME.log"
else
    SUBLOG=$(echo "$ENV_FILE" | awk -F '.' '{print $NF}')
    export LOG_FILE_NAME="$SUBLOG-run-$CURRENT_DATE_TIME.log"
fi

source ./logging.sh

if [ ! -f $ENV_FILE ]; then
    cp .envsample $ENV_FILE
    warn "Update $ENV_FILE with parameter values and run again"
    exit 1
fi

debug "Sourcing $ENV_FILE file"

set -a
source $ENV_FILE
set +a

section "Configuring AZ CLI"

if ! az account show &> /dev/null; then
    az login
fi

info "Setting Azure subscription to $AZURE_SUBSCRIPTIONID"
az account set --subscription "$AZURE_SUBSCRIPTIONID"

section "Running application"

source .venv/bin/activate

streamlit run src/app.py