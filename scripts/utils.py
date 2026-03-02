"""
Shared helper utilities used by all scripts in this project.

Provides: debug logging, execution pausing, timestamped log files,
config loading with profile support, and dependency checking.
"""

import importlib
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# ─── Project root ─────────────────────────────────────────────────────────────
# Finds the project root folder automatically, wherever this file lives.
PROJECT_ROOT = Path(__file__).parent.parent


# ─── Debug mode ───────────────────────────────────────────────────────────────

def is_debug_mode(args=None):
    """Returns True if debug mode is on via --debug flag or DEBUG=true env var."""
    if args and getattr(args, "debug", False):
        return True
    return os.environ.get("DEBUG", "").lower() in ("1", "true", "yes")


def debug_log(message, debug=False):
    """Prints a message only when debug mode is active."""
    if debug:
        print(f"[DEBUG] {message}")


def pause_if_debug(prompt="Press Enter to continue...", debug=False):
    """Pauses execution so you can inspect state when debug mode is active."""
    if debug:
        input(f"\n⏸  {prompt}\n")


# ─── Timestamped log file ─────────────────────────────────────────────────────

def setup_logger(script_name, debug=False):
    """
    Sets up a logger that writes to logs/<script_name>_<timestamp>.log.
    The logs/ folder is created automatically if it does not exist.
    Returns the logger object.
    """
    logs_dir = PROJECT_ROOT / "logs"
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"{script_name}_{timestamp}.log"

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        handlers=[logging.FileHandler(log_file, encoding="utf-8")],
    )

    logger = logging.getLogger(script_name)
    debug_log(f"Log file: {log_file}", debug)
    return logger


# ─── Config loading with profile support ─────────────────────────────────────

def load_config(profile=None, debug=False):
    """
    Loads config/settings.yaml from the project root.
    If a profile name is given (e.g. 'local' or 'cloud'), the matching
    config/profiles/<profile>.yaml is merged on top of the base settings.

    Returns a dict of config values.
    Prints a friendly message and exits if a required file is missing.
    """
    try:
        import yaml
    except ImportError:
        print("⚠️  PyYAML is not installed. Run: pip install pyyaml")
        sys.exit(1)

    config_dir = PROJECT_ROOT / "config"
    settings_file = config_dir / "settings.yaml"

    if not settings_file.exists():
        print(
            f"⚠️  Config file not found: {settings_file}\n"
            "    Copy config/template_settings.yaml to config/settings.yaml and fill it in."
        )
        sys.exit(1)

    with open(settings_file, encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    debug_log(f"Loaded base config from {settings_file}", debug)

    if profile:
        profile_file = config_dir / "profiles" / f"{profile}.yaml"
        if not profile_file.exists():
            print(
                f"⚠️  Profile file not found: {profile_file}\n"
                f"    Copy config/profiles/template_{profile}.yaml to {profile_file} and fill it in."
            )
            sys.exit(1)
        with open(profile_file, encoding="utf-8") as f:
            profile_data = yaml.safe_load(f) or {}
        config.update(profile_data)
        debug_log(f"Merged profile '{profile}' from {profile_file}", debug)

    return config


# ─── Dependency checking ──────────────────────────────────────────────────────

def check_dependencies(packages, debug=False):
    """
    Checks that a list of Python import names are available.
    Prints a friendly message and exits if any are missing.

    Usage: check_dependencies(["yaml", "requests"])
    """
    missing = []
    for package in packages:
        try:
            importlib.import_module(package)
            debug_log(f"  ✓ {package} found", debug)
        except ImportError:
            missing.append(package)
            debug_log(f"  ✗ {package} MISSING", debug)

    if missing:
        print("⚠️  Missing required packages. Install them with:\n")
        print(f"    pip install {' '.join(missing)}\n")
        sys.exit(1)

    debug_log("All dependencies found.", debug)
