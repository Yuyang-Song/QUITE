#!/bin/bash

# QUITE System Run Script - Hint Injection Only

# Load environment variables from .env file
if [ -f "../config_file/.env" ]; then
    source "../config_file/.env"
    echo "✅ Environment variables loaded from .env"
else
    echo "❌ Warning: .env file not found"
fi

# Path variables

INPUT_QUERIES="${PROJECT_ROOT}/dataset/queries/tpch_test.json"
SCHEMA_FILE="${PROJECT_ROOT}/dataset/schemas/tpch_schemas.sql"
OUTPUT_DIR="${PROJECT_ROOT}/output/test"

# Feature flags - only recommender enabled
ENABLE_RECOMMENDER="--enable_recommender"

# Execute - only hint injection/recommendation
python run.py \
    --input_path "${INPUT_QUERIES}" \
    --output_dir "${OUTPUT_DIR}" \
    --schema_file "${SCHEMA_FILE}" \
    ${ENABLE_RECOMMENDER}