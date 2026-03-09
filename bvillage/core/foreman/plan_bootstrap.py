# bvillage/core/foreman/plan_bootstrap.py
from __future__ import annotations

import importlib
import pkgutil

__all__ = ["ensure_plugins_loaded"]

_PLUGINS_LOADED = False


def _is_type_family_package(module_name: str) -> bool:
    parts = module_name.split(".")
    return len(parts) == 4 and parts[0] == "bvillage" and parts[1] == "types"


def ensure_plugins_loaded() -> None:
    """
    Import all concrete type-family plugins so they can register themselves.

    This function is idempotent and may be called multiple times.
    """
    global _PLUGINS_LOADED

    if _PLUGINS_LOADED:
        return

    package = importlib.import_module("bvillage.types")

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if not module.ispkg:
            continue

        name = module.name
        if not _is_type_family_package(name):
            continue

        importlib.import_module(name)

    _PLUGINS_LOADED = True
