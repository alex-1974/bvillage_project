# bvillage/core/plugin_loader.py

from __future__ import annotations

import importlib
import pkgutil

import bvillage.types


def load_type_plugins() -> None:
    """
    Import all type plugins so they can register themselves.

    This walks the bvillage.types package and imports every module
    that contains an __init__.py (i.e. a package).
    """

    package = bvillage.types

    for module in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        name = module.name

        # only load actual packages (type families)
        if module.ispkg:
            importlib.import_module(name)
