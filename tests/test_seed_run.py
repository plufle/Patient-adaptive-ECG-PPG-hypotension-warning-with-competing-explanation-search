import json
from pathlib import Path

import numpy as np

from dtwin.utils.config import load_config
from dtwin.utils.io import find_repo_root
from dtwin.utils.run import start_run
from dtwin.utils.seed import set_seed


def test_seed_is_reproducible():
    a = set_seed(123).normal(size=5)
    b = set_seed(123).normal(size=5)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, set_seed(124).normal(size=5))


def test_start_run_writes_config_and_meta(tmp_path: Path):
    cfg = load_config(find_repo_root() / "configs" / "base.yaml")
    r1 = start_run(cfg, "unit test", runs_dir=tmp_path)
    r2 = start_run(cfg, "unit test", runs_dir=tmp_path)  # same second: must not collide
    assert r1.dir != r2.dir
    assert load_config(r1.dir / "config.yaml") == cfg
    meta = json.loads((r1.dir / "meta.json").read_text(encoding="utf-8"))
    assert meta["seed"] == cfg["seed"]
    assert "commit" in meta["git"]
    r1.logger.info("hello")
    r1.close()
    r2.close()
    assert "hello" in (r1.dir / "run.log").read_text(encoding="utf-8")
