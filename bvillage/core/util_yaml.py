# bvillage/core/util_yaml.py
from __future__ import annotations

from pathlib import Path

import yaml

__all__ = ["load_yaml"]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise RuntimeError(f"YAML catalog must be a mapping: {path}")

    return data
