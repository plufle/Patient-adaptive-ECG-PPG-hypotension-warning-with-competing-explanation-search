"""Install the local git pre-commit hook that refuses notebooks with outputs.

Run once per clone: python scripts/install_hooks.py
"""

from pathlib import Path

HOOK = """#!/bin/sh
# Installed by scripts/install_hooks.py: refuse notebooks committed with outputs.
files=$(git diff --cached --name-only --diff-filter=ACM -- '*.ipynb')
[ -z "$files" ] && exit 0
python scripts/check_notebooks_clean.py $files
"""

repo = Path(__file__).resolve().parents[1]
hook_path = repo / ".git" / "hooks" / "pre-commit"
hook_path.write_text(HOOK, encoding="utf-8", newline="\n")
hook_path.chmod(0o755)
print(f"installed {hook_path}")
