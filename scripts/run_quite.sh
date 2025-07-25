#!/bin/bash

# QUITE System Run Script - Simple Configuration

# Load environment variables from .env file 
set -o allexport

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ENV_FILE="$SCRIPT_DIR/../config_file/.env"

if [[ -f "$ENV_FILE" ]]; then
    source "$ENV_FILE"
    echo "✅ Environment variables loaded from $ENV_FILE"
else
    echo "❌ Warning: $ENV_FILE not found"
fi

set +o allexport

# Path variables
INPUT_QUERIES="${PROJECT_ROOT}/dataset/queries/tpch_test.json"
SCHEMA_FILE="${PROJECT_ROOT}/dataset/schemas/tpch_schemas.sql"
OUTPUT_DIR="${PROJECT_ROOT}/output/test"

# Feature flags
ENABLE_REWRITER="--enable_rewriter"
ENABLE_RECOMMENDER="--enable_recommender"
SAVE_LOGS="--save_rewriter_logs"

# Execute
python run.py \
    --input_path "${INPUT_QUERIES}" \
    --output_dir "${OUTPUT_DIR}" \
    --schema_file "${SCHEMA_FILE}" \
    ${ENABLE_REWRITER} \
    ${ENABLE_RECOMMENDER} \
    ${SAVE_LOGS}

