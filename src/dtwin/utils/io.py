"""Path resolution that works the same on the local PC and on a Colab runtime.

Package code must never hardcode ``E:\\``, ``C:\\`` or ``/content`` paths; it asks
``get_paths()`` instead.

Resolution order for the storage root:

1. ``DTWIN_ROOT`` environment variable, if set.
2. On Colab: ``/content/drive/MyDrive/dtwin`` (Google Drive must be mounted).
3. Locally: the repository root (``data/`` and ``runs/`` are gitignored).

On Colab, ``scratch`` points to fast local disk (``/content/dtwin_scratch``),
which is wiped when the runtime disconnects. Copy heavy inputs there before
training; keep anything worth saving under ``root``.
"""

from __future__ import annotations

import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path

COLAB_DRIVE_ROOT = Path("/content/drive/MyDrive/dtwin")
COLAB_SCRATCH = Path("/content/dtwin_scratch")


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

    Raises:
        RuntimeError: on Colab when Google Drive is not mounted and no
            ``DTWIN_ROOT`` override is set (otherwise results would silently be
            written to disk that is wiped on disconnect).
    """
    env_root = os.environ.get("DTWIN_ROOT")
    if env_root:
        root = Path(env_root)
        scratch = Path(os.environ.get("DTWIN_SCRATCH", root / "scratch"))
    elif on_colab():
        if not COLAB_DRIVE_ROOT.parent.exists():
            raise RuntimeError(
                "Google Drive is not mounted. Run drive.mount('/content/drive'), "
                "or set DTWIN_ROOT to a non-persistent location explicitly."
            )
        root = COLAB_DRIVE_ROOT
        scratch = COLAB_SCRATCH
    else:
        root = find_repo_root()
        scratch = root / "data" / "scratch"

    paths = Paths(root=root, scratch=scratch)
    return paths.ensure() if create else paths
