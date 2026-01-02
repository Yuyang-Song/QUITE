"""
Module: path_config.py

Centralized path configuration for QUITE project.
This module ensures all paths are correctly resolved regardless of where the script is run from.
"""

import os
import sys
from pathlib import Path

def _find_project_root_by_structure() -> Path:
    """
    Find project root by looking for characteristic files/folders.
    """
    current = Path(__file__).resolve()
    
    # Navigate up until we find the project root (contains run.py and src/)
    for parent in [current] + list(current.parents):
        if (parent / "run.py").exists() and (parent / "src").exists():
            return parent
    
    # Fallback: assume this file is in src/utils/
    return Path(__file__).resolve().parents[2]

def _load_env_file_for_project_root() -> str:
    """
    Try to load PROJECT_ROOT from .env file before environment is fully set up.
    """
    # First find the project root by structure to locate .env
    root = _find_project_root_by_structure()
    env_file = root / "config_file" / ".env"
    
    if env_file.exists():
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('PROJECT_ROOT=') and not line.startswith('#'):
                        value = line.split('=', 1)[1].strip()
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        # Skip placeholder values
                        if not value.startswith('['):
                            return value
        except Exception:
            pass
    return None

def get_project_root() -> Path:
    """
    Get the project root directory (QUITE folder).
    This works regardless of where the script is executed from within the project.
    
    Priority:
    1. Environment variable PROJECT_ROOT (if already set)
    2. PROJECT_ROOT from .env file
    3. Auto-detect by directory structure
    
    Returns:
        Path: The absolute path to the project root directory
    """
    # First try environment variable (already set)
    if os.getenv("PROJECT_ROOT"):
        env_root = os.getenv("PROJECT_ROOT")
        if not env_root.startswith('['):  # Skip placeholder
            return Path(env_root)
    
    # Try to read from .env file directly
    env_root = _load_env_file_for_project_root()
    if env_root:
        return Path(env_root)
    
    # Fallback: find by directory structure
    return _find_project_root_by_structure()

# Project root path - computed once when module is loaded
PROJECT_ROOT = get_project_root()

# Common paths
CONFIG_PATH = PROJECT_ROOT / "config_file"
DATASET_PATH = PROJECT_ROOT / "dataset"
DOCUMENTS_PATH = PROJECT_ROOT / "documents"
EXPERIMENTS_PATH = PROJECT_ROOT / "experiments_results"
SRC_PATH = PROJECT_ROOT / "src"

def setup_python_path():
    """
    Add the project root to Python path to enable proper imports.
    Call this at the start of any script that needs to import from src/.
    """
    root_str = str(PROJECT_ROOT)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)

def get_env_file_path() -> Path:
    """Get the path to the .env file."""
    return CONFIG_PATH / ".env"

def load_project_env():
    """Load environment variables from the project's .env file."""
    from dotenv import load_dotenv
    env_path = get_env_file_path()
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        print(f"Warning: .env file not found at {env_path}")

# Auto-setup Python path when this module is imported
setup_python_path()
