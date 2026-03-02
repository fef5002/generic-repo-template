"""
generate_sidecars.py — Creates a small .yml metadata file (called a "sidecar")
next to every file in a target directory and all its sub-folders.

Each sidecar records the file's name, relative path, size, last-modified date,
and type.  This makes it easy to track and index files across local and cloud
storage without opening them.

Running this script more than once is safe — it only rewrites a sidecar when
the source file has actually changed (idempotent).

Usage:
    python scripts/generate_sidecars.py --dir /path/to/my/files
    python scripts/generate_sidecars.py --dir /path/to/my/files --debug
    python scripts/generate_sidecars.py --dir /path/to/my/files --profile cloud
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

# ─── Add project root to path so we can import shared utilities ───────────────
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from utils import debug_log, is_debug_mode, pause_if_debug, setup_logger

# Extensions that should never get a sidecar (skip sidecars and hidden files).
SKIP_EXTENSIONS = {".yml", ".yaml", ".gitignore"}


# ─── Build sidecar content ────────────────────────────────────────────────────

def build_sidecar_content(file_path: Path, base_dir: Path) -> str:
    """
    Builds the text content for a sidecar .yml file.
    Writes plain YAML (no library needed) so the format stays readable.
    """
    stat = file_path.stat()
    relative = file_path.relative_to(base_dir)
    modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    return (
        f"# Auto-generated sidecar — do not edit manually.\n"
        f"# Re-run generate_sidecars.py to refresh this file.\n"
        f"file: {file_path.name}\n"
        f"relative_path: {relative.as_posix()}\n"
        f"size_bytes: {stat.st_size}\n"
        f'last_modified: "{modified}"\n'
        f'file_type: "{file_path.suffix or "none"}"\n'
        f"tags: []\n"
        f'description: ""\n'
    )


# ─── Write one sidecar ────────────────────────────────────────────────────────

def generate_sidecar(file_path: Path, base_dir: Path, debug: bool = False) -> bool:
    """
    Creates or updates the .yml sidecar for a single file.
    Skips writing if the content has not changed (idempotent).
    Returns True when a sidecar was written, False when it was skipped.
    """
    sidecar_path = file_path.with_suffix(file_path.suffix + ".yml")
    content = build_sidecar_content(file_path, base_dir)

    if sidecar_path.exists() and sidecar_path.read_text(encoding="utf-8") == content:
        debug_log(f"Skipping unchanged: {sidecar_path.name}", debug)
        return False

    sidecar_path.write_text(content, encoding="utf-8")
    debug_log(f"Wrote: {sidecar_path}", debug)
    return True


# ─── Main scan loop ───────────────────────────────────────────────────────────

def run(target_dir: Path, debug: bool = False):
    """Walks target_dir and generates sidecars for every eligible file."""
    logger = setup_logger("generate_sidecars", debug)
    logger.info(f"Starting sidecar generation in: {target_dir}")

    if not target_dir.exists():
        print(f"⚠️  Directory not found: {target_dir}")
        sys.exit(1)

    # Collect all files, excluding sidecar files themselves and .git internals.
    files = [
        f
        for f in target_dir.rglob("*")
        if f.is_file()
        and f.suffix not in SKIP_EXTENSIONS
        and ".git" not in f.parts
    ]

    print(f"Found {len(files)} file(s) to process in: {target_dir}")
    pause_if_debug("Review the file count above, then press Enter to start.", debug)

    written = 0
    skipped = 0
    for file_path in files:
        debug_log(f"Processing: {file_path}", debug)
        pause_if_debug(f"About to write sidecar for: {file_path.name}", debug)
        if generate_sidecar(file_path, target_dir, debug):
            written += 1
        else:
            skipped += 1

    logger.info(f"Done. Written={written}, Skipped={skipped}")
    print(f"✅  Done — {written} sidecar(s) written, {skipped} unchanged.")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate .yml sidecar metadata files for every file in a directory."
    )
    parser.add_argument(
        "--dir",
        required=True,
        help="Folder to scan (e.g. /path/to/my/files or a mounted cloud drive).",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print step-by-step output and pause at key checkpoints.",
    )
    parser.add_argument(
        "--profile",
        default=None,
        help="Config profile to load, e.g. 'local' or 'cloud'.",
    )
    args = parser.parse_args()
    debug = is_debug_mode(args)

    target_dir = Path(args.dir).resolve()
    debug_log(f"Target directory resolved to: {target_dir}", debug)

    run(target_dir, debug)


if __name__ == "__main__":
    main()
