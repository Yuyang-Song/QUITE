#!/bin/bash

# QUITE Performance Evaluation Script
#
# Usage:
#   bash ./scripts/evaluation.sh              # Normal mode (with database restart)
#   bash ./scripts/evaluation.sh --no_restart # No-restart mode (for restricted environments)
#
# IMPORTANT: Database Restart Requirement
# ========================================
# By default, this script restarts PostgreSQL between query executions to clear
# database caches for fair performance comparison. This requires system permissions:
#   - Linux: sudo systemctl restart postgresql
#   - macOS: brew services restart postgresql
#
# If you don't have restart permissions (shared/cloud database), use --no_restart:
#   bash ./scripts/evaluation.sh --no_restart
#
# The --no_restart mode:
#   - Skips database restart operations
#   - Runs each query 5 times instead of 3
#   - Removes highest and lowest execution times
#   - Averages remaining 3 runs to mitigate cold-start effects

# Source the common environment setup
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/setup_env.sh"

# Path variables (now using PROJECT_ROOT from setup_env.sh)
QUERIES_PATH="${PROJECT_ROOT}/output/test/rewritten_queries.json"
STORAGE_PATH="${PROJECT_ROOT}/experiments_results/EXP_result_test.json"
FILTERED_PATH="${PROJECT_ROOT}/experiments_results/filtered_result_test.json"
TIMEOUT=300

# Check for --no_restart flag
NO_RESTART_FLAG=""
if [[ "$1" == "--no_restart" ]]; then
    NO_RESTART_FLAG="--no_restart"
    echo "🔄 Running in NO-RESTART mode"
fi

# Execute evaluation
python evaluation.py \
    -q "${QUERIES_PATH}" \
    -s "${STORAGE_PATH}" \
    -f "${FILTERED_PATH}" \
    -t ${TIMEOUT} \
    ${NO_RESTART_FLAG}