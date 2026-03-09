# bvillage/foreman/plan_bootstrap.py
from __future__ import annotations

import importlib
import pkgutil

import bvillage.types

__all__ = ["ensure_plugins_loaded"]

_PLUGINS_LOADED = False


def _is_type_family_package(module_name: str) -> bool:
    """
    Accept only packages shaped like:

        bvillage.types.<domain>.<family>

    Examples
    --------
    valid:
        bvillage.types.timber_frame.longhouse
        bvillage.types.timber_frame.townhouse

    invalid:
        bvillage.types
        bvillage.types.timber_frame
        bvillage.types.timber_frame.longhouse.contracts
        bvillage.types.helpers
    """
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

    package = bvillage.types

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if not module.ispkg:
            continue

        name = module.name
        if not _is_type_family_package(name):
            continue

        importlib.import_module(name)

    _PLUGINS_LOADED = True
