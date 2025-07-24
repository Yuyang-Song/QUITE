#!/bin/bash

# QUITE System Run Script - Query Rewrite Only

# Path variables
QUITE_ROOT="/root/syy/QUITE"
INPUT_QUERIES="${QUITE_ROOT}/dataset/queries/tpch_test.json"
SCHEMA_FILE="${QUITE_ROOT}/dataset/schemas/tpch_schemas.sql"
OUTPUT_DIR="${QUITE_ROOT}/output/test"

# Feature flags - only rewriter enabled
ENABLE_REWRITER="--enable_rewriter"

# Execute - only query rewriting
python run.py \
    --input_path "${INPUT_QUERIES}" \
    --output_dir "${OUTPUT_DIR}" \
    --schema_file "${SCHEMA_FILE}" \
    ${ENABLE_REWRITER}