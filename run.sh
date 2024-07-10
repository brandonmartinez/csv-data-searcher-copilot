#!/usr/bin/env bash

if [ ! -f .env ]; then
    cp .envsample .env
    echo "Warning: .env file not found. Copied .envsample as .env; please update with your values."
    exit 1
fi

set -eo pipefail
set -a

source .env

set +a

source .venv/bin/activate

python src/app.py