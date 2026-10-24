"""Run bookkeeping: every experiment gets a run directory with everything needed to reproduce it.

A run directory ``runs/<YYYYmmdd-HHMMSS>_<name>/`` contains:

- ``config.yaml``: the fully resolved config;
- ``meta.json``: git commit (and whether the tree had uncommitted changes),
  seed, Python version, platform and key package versions;
- ``run.log``: the log file.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from importlib import metadata
from logging import Logger
from pathlib import Path

from .config import dump_config
from .io import find_repo_root, get_paths
from .log import get_logger

_TRACKED_PACKAGES = ("numpy", "scipy", "pandas", "torch", "sbi", "lightgbm", "neurokit2", "vitaldb", "wfdb")


@dataclass
class Run:
    run_id: str
    dir: Path
    config: dict
    logger: Logger

    def close(self) -> None:
        """Flush and detach the run's log handlers (releases the log file, needed on Windows)."""
        for handler in list(self.logger.handlers):
            handler.flush()
            handler.close()
            self.logger.removeHandler(handler)


def git_state(repo: Path | None = None) -> dict:
    """Return ``{'commit': sha or None, 'dirty': bool or None}`` without failing if git is absent."""
    try:
        repo = repo or find_repo_root()
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True
        ).stdout.strip()
        status = subprocess.run(
            ["git", "status", "--porcelain"], cwd=repo, capture_output=True, text=True, check=True
        ).stdout
        return {"commit": commit, "dirty": bool(status.strip())}
    except (OSError, subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": None, "dirty": None}


def _package_versions() -> dict:
    versions = {}
    for name in _TRACKED_PACKAGES:
        try:
            versions[name] = metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return versions


def start_run(config: dict, name: str, runs_dir: Path | None = None) -> Run:
    """Create a run directory, save config and metadata, and return a Run with its logger."""
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name)
    base = runs_dir or get_paths(create=True).runs
    base.mkdir(parents=True, exist_ok=True)
    run_id = f"{stamp}_{safe_name}"
    suffix = 1
    while (base / run_id).exists():  # two runs started in the same second
        suffix += 1
        run_id = f"{stamp}_{safe_name}_{suffix}"
    run_dir = base / run_id
    run_dir.mkdir()

    dump_config(config, run_dir / "config.yaml")
    meta = {
        "run_id": run_id,
        "name": name,
        "started": datetime.now().isoformat(timespec="seconds"),
        "seed": config.get("seed"),
        "git": git_state(),
        "python": sys.version,
        "platform": platform.platform(),
        "packages": _package_versions(),
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    logger = get_logger(f"dtwin.run.{run_id}", log_file=run_dir / "run.log")
    if meta["git"]["dirty"]:
        logger.warning("Uncommitted changes present: results may not be reproducible from the commit hash.")
    logger.info("Run %s started in %s", run_id, run_dir)
    return Run(run_id=run_id, dir=run_dir, config=config, logger=logger)
