#!/bin/bash

# QUITE Performance Evaluation Script

# Source the common environment setup
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/setup_env.sh"

# Path variables (now using PROJECT_ROOT from setup_env.sh)
QUERIES_PATH="${PROJECT_ROOT}/output/test/rewritten_queries.json"
STORAGE_PATH="${PROJECT_ROOT}/experiments_results/EXP_result_test.json"
FILTERED_PATH="${PROJECT_ROOT}/experiments_results/filtered_result_test.json"
TIMEOUT=300

# Execute evaluation
python evaluation.py \
    -q "${QUERIES_PATH}" \
    -s "${STORAGE_PATH}" \
    -f "${FILTERED_PATH}" \
    -t ${TIMEOUT}