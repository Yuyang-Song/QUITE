#!/bin/bash

# Common environment setup script for QUITE project
# This script can be sourced from any location and will correctly set up the environment

# Find the project root directory (where run.py is located)
find_project_root() {
    local current_dir="$1"
    
    # Check if we're already at project root
    if [[ -f "$current_dir/run.py" && -d "$current_dir/src" ]]; then
        echo "$current_dir"
        return 0
    fi
    
    # Try to find from script directory (if sourced from scripts/)
    local script_parent="$(dirname "$current_dir")"
    if [[ -f "$script_parent/run.py" && -d "$script_parent/src" ]]; then
        echo "$script_parent"
        return 0
    fi
    
    # Search upward from current working directory
    local search_dir="$(pwd)"
    while [[ "$search_dir" != "/" ]]; do
        if [[ -f "$search_dir/run.py" && -d "$search_dir/src" ]]; then
            echo "$search_dir"
            return 0
        fi
        search_dir="$(dirname "$search_dir")"
    done
    
    return 1
}

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Find project root
PROJECT_ROOT="$(find_project_root "$SCRIPT_DIR")"

if [[ -z "$PROJECT_ROOT" ]]; then
    echo "❌ Error: Could not find QUITE project root directory"
    echo "Please run this script from within the QUITE project directory"
    exit 1
fi

export PROJECT_ROOT
echo "📁 Project root: $PROJECT_ROOT"

# Load environment variables from .env file
ENV_FILE="$PROJECT_ROOT/config_file/.env"
if [[ -f "$ENV_FILE" ]]; then
    set -o allexport
    source "$ENV_FILE"
    set +o allexport
    echo "✅ Environment variables loaded from $ENV_FILE"
else
    echo "⚠️  Warning: $ENV_FILE not found"
fi

# Change to project root directory so Python imports work correctly
cd "$PROJECT_ROOT"
echo "📂 Working directory: $(pwd)"
