#!/bin/bash

# QUITE Performance Evaluation Script

# Make sure you execute this script in the QUITE root directory like: /root/exp/QUITE/

# Usage: bash ./scripts/evaluation.sh
QUERIES_PATH="./output/test/rewritten_queries.json"
STORAGE_PATH="./experiments_results/EXP_result_test.json"
FILTERED_PATH="./experiments_results/filtered_result_test.json"
TIMEOUT=300

# Execute evaluation
python evaluation.py \
    -q "${QUERIES_PATH}" \
    -s "${STORAGE_PATH}" \
    -f "${FILTERED_PATH}" \
    -t ${TIMEOUT}