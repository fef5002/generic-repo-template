"""
check_dependencies.py — Checks that all required Python packages listed in
requirements.txt are installed before you run any other script.

Run this first when setting up a new environment to catch missing packages
before they cause confusing errors later.

Usage:
    python scripts/check_dependencies.py
    python scripts/check_dependencies.py --debug
    python scripts/check_dependencies.py --requirements /path/to/requirements.txt
"""

import argparse
import importlib
import sys
from pathlib import Path

# ─── Add project root to path so we can import shared utilities ───────────────
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils import debug_log, is_debug_mode

# Maps pip install names to their Python import names (they sometimes differ).
IMPORT_NAME_MAP = {
    "pyyaml": "yaml",
    "python-dotenv": "dotenv",
    "pillow": "PIL",
    "scikit-learn": "sklearn",
    "opencv-python": "cv2",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────

def pip_to_import_name(pip_name: str) -> str:
    """
    Converts a pip package name (e.g. 'pyyaml') to its Python import name
    (e.g. 'yaml').  Falls back to the pip name itself if no mapping is known.
    """
    # Strip version specifiers like ==1.2.3 or >=2.0
    clean = pip_name.split("==")[0].split(">=")[0].split("<=")[0].strip().lower()
    return IMPORT_NAME_MAP.get(clean, clean)


# ─── Main check ───────────────────────────────────────────────────────────────

def check_requirements_file(req_file: Path, debug: bool = False):
    """
    Reads a requirements.txt, tries to import each package, and prints a
    clear pass/fail summary.  Exits with an error if anything is missing.
    """
    if not req_file.exists():
        print(f"⚠️  Requirements file not found: {req_file}")
        sys.exit(1)

    lines = req_file.read_text(encoding="utf-8").splitlines()
    # Skip blank lines and comments
    packages = [line.strip() for line in lines if line.strip() and not line.startswith("#")]

    if not packages:
        print("No packages listed in requirements.txt — nothing to check.")
        return

    print(f"Checking {len(packages)} package(s) from {req_file.name}...\n")

    missing = []
    for pip_name in packages:
        import_name = pip_to_import_name(pip_name)
        debug_log(f"Trying to import '{import_name}' (pip: {pip_name})", debug)
        try:
            importlib.import_module(import_name)
            print(f"  ✓  {pip_name}")
        except ImportError:
            missing.append(pip_name)
            print(f"  ✗  {pip_name}  ← MISSING")

    print()
    if missing:
        print(f"⚠️  {len(missing)} package(s) missing. Install them with:\n")
        print(f"    pip install {' '.join(missing)}\n")
        sys.exit(1)
    else:
        print(f"✅  All {len(packages)} package(s) are installed.")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check that all required Python packages are installed."
    )
    parser.add_argument(
        "--requirements",
        default=str(PROJECT_ROOT / "requirements.txt"),
        help="Path to requirements.txt (default: project root).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show the import name used for each package.",
    )
    args = parser.parse_args()
    debug = is_debug_mode(args)

    req_file = Path(args.requirements).resolve()
    debug_log(f"Requirements file: {req_file}", debug)

    check_requirements_file(req_file, debug)


if __name__ == "__main__":
    main()
