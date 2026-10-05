#!/usr/bin/env python3
"""Maintain local_memory metadata for each pipeline run.

Default behavior:
- target: local_memory
- write/update local_memory/sync_manifest.json
- keep local sync metadata files in target
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


PROTECTED_TARGET_FILES = {"sync_manifest.json", "README.md"}


def _files_under(root: Path) -> list[Path]:
    return [p for p in root.rglob("*") if p.is_file()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Update local_memory sync manifest")
    parser.add_argument("--target-dir", default="local_memory", help="Target local memory directory")
    parser.add_argument("--quiet", action="store_true", help="Print summary only")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    target_dir = (repo_root / args.target_dir).resolve()

    target_dir.mkdir(parents=True, exist_ok=True)

    all_files = _files_under(target_dir)
    data_files = [p for p in all_files if p.relative_to(target_dir).as_posix() not in PROTECTED_TARGET_FILES]

    manifest = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_dir": str(target_dir),
        "mode": "local_memory_only",
        "file_count": len(data_files),
    }
    (target_dir / "sync_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Memory sync: PASS (local files={len(data_files)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
