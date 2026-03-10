# bvillage/core/plugin_bootstrap.py

from __future__ import annotations

import importlib
import pkgutil

__all__ = ["ensure_plugins_loaded"]

_PLUGINS_LOADED = False


def _iter_plugin_packages(package_name: str, *, depth: int):
    """
    Yield package module names at exactly the requested depth.

    Examples
    --------
    package_name="bvillage.domains", depth=1
        -> bvillage.domains.<domain>

    package_name="bvillage.types", depth=2
        -> bvillage.types.<domain>.<type>
    """
    package = importlib.import_module(package_name)
    base_parts = package_name.count(".")

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        if not module.ispkg:
            continue

        parts = module.name.count(".") - base_parts
        if parts == depth:
            yield module.name


def _load_register_functions(package_name: str, *, depth: int) -> None:
    for module_name in _iter_plugin_packages(package_name, depth=depth):
        mod = importlib.import_module(module_name)
        register = getattr(mod, "register", None)
        if callable(register):
            register()


def ensure_plugins_loaded() -> None:
    """
    Load all BVILLAGE plugins exactly once.

    Architecture
    ------------
    Core must not know concrete types or domains.
    Plugins register themselves via `register()`.

    Discovery policy
    ----------------
    - domains: load first-level packages under bvillage.domains
      e.g. bvillage.domains.timber_frame

    - types: load second-level packages under bvillage.types
      e.g. bvillage.types.timber_frame.longhouse

    This avoids importing deep submodules like domain blender files.
    """
    global _PLUGINS_LOADED

    if _PLUGINS_LOADED:
        return

    _load_register_functions("bvillage.domains", depth=1)
    _load_register_functions("bvillage.types", depth=2)

    _PLUGINS_LOADED = True
