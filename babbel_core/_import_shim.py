import os, sys

# Ensure both repo root and package dir are on sys.path
FILE_DIR = os.path.dirname(__file__)
PKG_ROOT = FILE_DIR                              # .../babbel_core
REPO_ROOT = os.path.abspath(os.path.join(FILE_DIR, '..'))  # repo root
for p in (PKG_ROOT, REPO_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

# Try imports for BOTH execution contexts (local & Streamlit Cloud)
try:
    from core.pipeline import run_pipeline
    from core.rewrite import rewrite_tone, enforce_babbel_style
except ModuleNotFoundError:
    from babbel_core.core.pipeline import run_pipeline      # when run from repo root
    from babbel_core.core.rewrite import rewrite_tone, enforce_babbel_style

__all__ = ["run_pipeline", "rewrite_tone", "enforce_babbel_style"]
