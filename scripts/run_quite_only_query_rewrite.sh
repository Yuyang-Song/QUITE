#!/bin/bash

# QUITE System Run Script - Query Rewrite Only

# Source the common environment setup
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/setup_env.sh"

# Path variables (now using PROJECT_ROOT from setup_env.sh)
INPUT_QUERIES="${PROJECT_ROOT}/dataset/queries/tpch_test.json"
SCHEMA_FILE="${PROJECT_ROOT}/dataset/schemas/tpch_schemas.sql"
OUTPUT_DIR="${PROJECT_ROOT}/output/test"

# Feature flags - only rewriter enabled
ENABLE_REWRITER="--enable_rewriter"

# Execute - only query rewriting
python run.py \
    --input_path "${INPUT_QUERIES}" \
    --output_dir "${OUTPUT_DIR}" \
    --schema_file "${SCHEMA_FILE}" \
    ${ENABLE_REWRITER}