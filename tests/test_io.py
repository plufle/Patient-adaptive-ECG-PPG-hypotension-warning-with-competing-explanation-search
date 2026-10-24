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


def test_colab_without_drive_raises(monkeypatch):
    monkeypatch.delenv("DTWIN_ROOT", raising=False)
    monkeypatch.setattr(io, "on_colab", lambda: True)
    monkeypatch.setattr(io, "COLAB_DRIVE_ROOT", Path("/definitely/not/mounted/dtwin"))
    try:
        io.get_paths()
    except RuntimeError as e:
        assert "Drive" in str(e)
    else:
        raise AssertionError("expected RuntimeError when Drive is not mounted")
