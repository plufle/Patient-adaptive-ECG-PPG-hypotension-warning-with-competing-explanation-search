"""Path resolution that works the same on the local PC and on a Colab runtime.

Package code must never hardcode ``E:\\``, ``C:\\`` or ``/content`` paths; it asks
``get_paths()`` instead.

Storage model ("plan B", CLAUDE.md §6): the **local PC is the persistent home**
of all data and results. Colab is used for GPU compute only, and its disk is
temporary. Google Drive cannot be mounted through the Colab VS Code extension.

Resolution order for the storage root:

1. ``DTWIN_ROOT`` environment variable, if set.
2. On Colab: ``/content/dtwin``. This is **temporary**: it is wiped when the
   runtime disconnects. Anything worth keeping must be brought back to the PC.
3. Locally: the repository root (``data/`` and ``runs/`` are gitignored).
"""

from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path

COLAB_ROOT = Path("/content/dtwin")


def on_colab() -> bool:
    """True when running on a Colab runtime (including via the VS Code extension)."""
    if "COLAB_RELEASE_TAG" in os.environ or "COLAB_GPU" in os.environ:
        return True
    try:
        return importlib.util.find_spec("google.colab") is not None
    except ModuleNotFoundError:  # "google" namespace absent
        return False


def find_repo_root(start: Path | None = None) -> Path:
    """Walk up from ``start`` (default: this file) to the directory holding pyproject.toml."""
    here = (start or Path(__file__)).resolve()
    for parent in [here, *here.parents]:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise FileNotFoundError("Could not find the repository root (no pyproject.toml found).")


@dataclass(frozen=True)
class Paths:
    """All storage locations used by the project."""

    root: Path
    scratch: Path
    persistent: bool  # False on Colab: everything here is lost on disconnect

    @property
    def data(self) -> Path:
        return self.root / "data"

    @property
    def raw(self) -> Path:
        return self.data / "raw"

    @property
    def processed(self) -> Path:
        return self.data / "processed"

    @property
    def splits(self) -> Path:
        return self.data / "splits"

    @property
    def runs(self) -> Path:
        return self.root / "runs"

    def ensure(self) -> "Paths":
        """Create every directory (idempotent) and return self."""
        for p in (self.raw, self.processed, self.splits, self.runs, self.scratch):
            p.mkdir(parents=True, exist_ok=True)
        return self


def get_paths(create: bool = False) -> Paths:
    """Resolve project paths for the current environment.

    Args:
        create: if True, create the directories.
    """
    env_root = os.environ.get("DTWIN_ROOT")
    if env_root:
        root = Path(env_root)
        persistent = os.environ.get("DTWIN_PERSISTENT", "0" if on_colab() else "1") == "1"
    elif on_colab():
        root = COLAB_ROOT
        persistent = False
    else:
        root = find_repo_root()
        persistent = True

    paths = Paths(root=root, scratch=root / "data" / "scratch", persistent=persistent)
    return paths.ensure() if create else paths
