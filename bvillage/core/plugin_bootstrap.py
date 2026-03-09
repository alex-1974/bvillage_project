from __future__ import annotations

import importlib

__all__ = ["ensure_plugins_loaded"]

_PLUGINS_LOADED = False


def ensure_plugins_loaded() -> None:
    global _PLUGINS_LOADED

    if _PLUGINS_LOADED:
        return

    # ------------------------------------------------------------
    # Type plugins
    # ------------------------------------------------------------
    importlib.import_module("bvillage.types.timber_frame.longhouse").register()

    # ------------------------------------------------------------
    # Domain plugins
    # ------------------------------------------------------------
    importlib.import_module("bvillage.domains.timber_frame").register()

    _PLUGINS_LOADED = True
