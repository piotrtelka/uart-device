#!/bin/bash

set -e

if [ ! -f .env ]; then
    echo "No .env file"
else
    echo "Loading .env file"
    source .env
fi

uvicorn app.main:app --host "${HOST}" --port "${PORT}"
