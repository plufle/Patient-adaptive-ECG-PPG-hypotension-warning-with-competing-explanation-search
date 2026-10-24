from pathlib import Path

import pytest

from dtwin.utils.config import deep_merge, dump_config, get_by_path, load_config
from dtwin.utils.io import find_repo_root

BASE = find_repo_root() / "configs" / "base.yaml"


def test_base_config_has_provisional_values():
    cfg = load_config(BASE)
    assert get_by_path(cfg, "events.map_threshold_mmhg") == 65
    assert get_by_path(cfg, "task.warn_interval_min") == [10, 15]
    assert abs(sum(cfg["splits"]["ratios"].values()) - 1.0) < 1e-9


def test_overrides_are_parsed_as_yaml():
    cfg = load_config(BASE, ["events.map_threshold_mmhg=60", "seed=7", "task.warn_interval_min=[5, 10]"])
    assert cfg["events"]["map_threshold_mmhg"] == 60
    assert cfg["seed"] == 7
    assert cfg["task"]["warn_interval_min"] == [5, 10]


def test_bad_override_rejected():
    with pytest.raises(ValueError):
        load_config(BASE, ["no_equals_sign"])


def test_extends_deep_merges(tmp_path: Path):
    (tmp_path / "parent.yaml").write_text("a: {x: 1, y: 2}\nb: 3\n", encoding="utf-8")
    (tmp_path / "child.yaml").write_text("extends: parent.yaml\na: {y: 20}\n", encoding="utf-8")
    cfg = load_config(tmp_path / "child.yaml")
    assert cfg == {"a": {"x": 1, "y": 20}, "b": 3}


def test_circular_extends_detected(tmp_path: Path):
    (tmp_path / "a.yaml").write_text("extends: b.yaml\n", encoding="utf-8")
    (tmp_path / "b.yaml").write_text("extends: a.yaml\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_config(tmp_path / "a.yaml")


def test_dump_roundtrip(tmp_path: Path):
    cfg = load_config(BASE)
    dump_config(cfg, tmp_path / "out.yaml")
    assert load_config(tmp_path / "out.yaml") == cfg


def test_deep_merge_does_not_mutate_inputs():
    base = {"a": {"x": 1}}
    deep_merge(base, {"a": {"x": 2}})
    assert base == {"a": {"x": 1}}


def test_get_by_path_default():
    assert get_by_path({"a": {}}, "a.b", default=None) is None
    with pytest.raises(KeyError):
        get_by_path({"a": {}}, "a.b")
