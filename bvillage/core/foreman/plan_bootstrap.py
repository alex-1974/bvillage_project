"""
bvillage/core/foreman/plan_bootstrap.py

Plugin bootstrap loader.

Loads all domain and type plugins and executes their register()
functions if present.
"""

from __future__ import annotations

import importlib
import pkgutil

_BOOTSTRAPPED = False


def ensure_plugins_loaded() -> None:
    global _BOOTSTRAPPED

    if _BOOTSTRAPPED:
        return

    _load_package_plugins("bvillage.types")
    _load_package_plugins("bvillage.domains")

    _BOOTSTRAPPED = True


def _load_package_plugins(package_name: str) -> None:

    package = importlib.import_module(package_name)

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):

        mod = importlib.import_module(module.name)

        register = getattr(mod, "register", None)

        if callable(register):
            register()
