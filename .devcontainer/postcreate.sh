#!/usr/bin/env bash

if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment"
    python -m venv .venv
fi

echo "Activating Python virtual environment"
source .venv/bin/activate

echo "Upgrading pip"
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies"
    pip install -r requirements.txt
fi
