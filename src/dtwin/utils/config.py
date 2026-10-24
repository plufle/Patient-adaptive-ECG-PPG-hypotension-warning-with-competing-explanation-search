"""YAML configs with inheritance and command-line style overrides.

A config file may name a parent with ``extends: <relative path>``; the child's
keys are deep-merged over the parent's. Overrides use dotted keys, e.g.
``["events.map_threshold_mmhg=60", "seed=7"]``; values are parsed as YAML, so
numbers, booleans, lists and null work as expected.

Every [PROVISIONAL] value from CLAUDE.md lives in ``configs/base.yaml`` so that
nothing is a hidden constant in code.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Iterable

import yaml

_MISSING = object()


def deep_merge(base: dict, override: dict) -> dict:
    """Return a new dict with ``override`` merged into ``base`` (nested dicts merge, others replace)."""
    out = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = copy.deepcopy(value)
    return out


def _load_with_extends(path: Path, seen: set[Path]) -> dict:
    path = path.resolve()
    if path in seen:
        raise ValueError(f"Circular 'extends' chain at {path}")
    seen.add(path)
    with path.open("r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    if not isinstance(cfg, dict):
        raise ValueError(f"Top level of {path} must be a mapping")
    parent = cfg.pop("extends", None)
    if parent is None:
        return cfg
    return deep_merge(_load_with_extends(path.parent / parent, seen), cfg)


def set_by_path(cfg: dict, dotted_key: str, value: Any) -> None:
    """Set ``cfg['a']['b'] = value`` for ``dotted_key='a.b'``, creating levels as needed."""
    keys = dotted_key.split(".")
    node = cfg
    for k in keys[:-1]:
        node = node.setdefault(k, {})
        if not isinstance(node, dict):
            raise KeyError(f"Cannot descend into non-mapping at '{k}' in '{dotted_key}'")
    node[keys[-1]] = value


def get_by_path(cfg: dict, dotted_key: str, default: Any = _MISSING) -> Any:
    """Read ``cfg['a']['b']`` for ``dotted_key='a.b'``; raise KeyError unless a default is given."""
    node: Any = cfg
    for k in dotted_key.split("."):
        if not isinstance(node, dict) or k not in node:
            if default is _MISSING:
                raise KeyError(dotted_key)
            return default
        node = node[k]
    return node


def load_config(path: str | Path, overrides: Iterable[str] = ()) -> dict:
    """Load a YAML config (following ``extends``) and apply ``key=value`` overrides."""
    cfg = _load_with_extends(Path(path), set())
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"Override must look like key=value, got '{item}'")
        key, raw = item.split("=", 1)
        set_by_path(cfg, key.strip(), yaml.safe_load(raw))
    return cfg


def dump_config(cfg: dict, path: str | Path) -> None:
    """Write the fully resolved config, so a run can be reproduced exactly."""
    with Path(path).open("w", encoding="utf-8") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
