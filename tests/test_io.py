from pathlib import Path

from dtwin.utils import io


def test_env_override(monkeypatch, tmp_path: Path):
    monkeypatch.setenv("DTWIN_ROOT", str(tmp_path))
    paths = io.get_paths(create=True)
    assert paths.root == tmp_path
    assert paths.runs == tmp_path / "runs"
    assert paths.raw.is_dir() and paths.processed.is_dir() and paths.splits.is_dir()


def test_local_default_is_repo_root(monkeypatch):
    monkeypatch.delenv("DTWIN_ROOT", raising=False)
    monkeypatch.setattr(io, "on_colab", lambda: False)
    paths = io.get_paths()
    assert (paths.root / "pyproject.toml").is_file()
    assert paths.data == paths.root / "data"


def test_colab_default_is_temporary(monkeypatch):
    monkeypatch.delenv("DTWIN_ROOT", raising=False)
    monkeypatch.setattr(io, "on_colab", lambda: True)
    paths = io.get_paths()
    assert paths.root == io.COLAB_ROOT
    assert paths.persistent is False


def test_local_default_is_persistent(monkeypatch):
    monkeypatch.delenv("DTWIN_ROOT", raising=False)
    monkeypatch.setattr(io, "on_colab", lambda: False)
    assert io.get_paths().persistent is True
