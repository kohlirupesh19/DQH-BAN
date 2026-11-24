"""
dashboard/utils/path_manager.py
Robust cross-platform path resolution for DQH-BAN dashboard.
Eliminates hardcoded paths and supports local and cloud deployments.
"""

import os
from pathlib import Path

# Repository root directory
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def get_repo_root() -> Path:
    return REPO_ROOT

def get_artifacts_dir() -> Path:
    return REPO_ROOT / "artifacts"

def get_results_dir() -> Path:
    return REPO_ROOT / "artifacts" / "results"

def get_thresholds_dir() -> Path:
    return REPO_ROOT / "artifacts" / "thresholds"

def get_figures_dir() -> Path:
    return REPO_ROOT / "figures"

def get_reports_dir() -> Path:
    return REPO_ROOT / "reports"

def get_assets_dir() -> Path:
    return REPO_ROOT / "dashboard" / "assets"

def get_styles_dir() -> Path:
    return REPO_ROOT / "dashboard" / "styles"

def resolve_path(rel_path: str) -> Path:
    """Safely resolves relative paths against repository root."""
    # Strip any leading slashes or accidental absolute references
    clean_p = rel_path.lstrip("/").lstrip("\\")
    if "Volumes" in clean_p or "Users" in clean_p:
        # Fallback to base name if old full path was passed
        clean_p = os.path.basename(clean_p)
    full_p = REPO_ROOT / clean_p
    return full_p
