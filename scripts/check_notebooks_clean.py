"""Fail if any given notebook contains cell outputs or execution counts.

Used by the local git pre-commit hook (install with ``python scripts/install_hooks.py``)
so notebooks run in VS Code are never committed with their outputs.

Usage: python scripts/check_notebooks_clean.py [--strip] NOTEBOOK [NOTEBOOK ...]
  --strip   remove outputs in place instead of failing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def is_dirty(nb: dict) -> bool:
    return any(
        cell.get("outputs") or cell.get("execution_count") is not None
        for cell in nb.get("cells", [])
        if cell.get("cell_type") == "code"
    )


def strip(nb: dict) -> dict:
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
    return nb


def main(argv: list[str]) -> int:
    do_strip = "--strip" in argv
    paths = [Path(a) for a in argv if a != "--strip"]
    dirty = []
    for path in paths:
        nb = json.loads(path.read_text(encoding="utf-8"))
        if not is_dirty(nb):
            continue
        if do_strip:
            path.write_text(json.dumps(strip(nb), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"stripped outputs: {path}")
        else:
            dirty.append(path)
    if dirty:
        print("Notebooks contain outputs (commit refused):")
        for p in dirty:
            print(f"  {p}")
        print("Strip them with: python scripts/check_notebooks_clean.py --strip <files>, then re-add.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
