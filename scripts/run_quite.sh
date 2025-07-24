#!/bin/bash

# QUITE System Run Script - Simple Configuration

# Path variables
INPUT_QUERIES="/root/syy/QUITE/dataset/queries/tpch_test.json"
SCHEMA_FILE="/root/syy/QUITE/dataset/schemas/tpch_schemas.sql"
OUTPUT_DIR="/root/syy/QUITE/output/test"

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

