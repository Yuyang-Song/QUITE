#!/bin/bash

# QUITE System Run Script - Hint Injection Only

# Path variables
INPUT_QUERIES="/root/syy/QUITE/dataset/queries/tpch_test.json"
SCHEMA_FILE="/root/syy/QUITE/dataset/schemas/tpch_schemas.sql"
OUTPUT_DIR="/root/syy/QUITE/output/test"

# Feature flags - only recommender enabled
ENABLE_RECOMMENDER="--enable_recommender"

# Execute - only hint injection/recommendation
python run.py \
    --input_path "${INPUT_QUERIES}" \
    --output_dir "${OUTPUT_DIR}" \
    --schema_file "${SCHEMA_FILE}" \
    ${ENABLE_RECOMMENDER}