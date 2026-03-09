from __future__ import annotations

from pathlib import Path

from bvillage.core.dispatch_registry import register_provider_with_archetypes
from bvillage.core.schema_i18n import register_locale_catalog

from .provider import LonghouseTypeProvider

__all__ = ["LonghouseTypeProvider", "register"]


def _try_register_locales() -> None:
    """
    Best-effort locale registration.

    WHY:
    The build pipeline must not depend on optional YAML support.
    Blender runtime environments may not have PyYAML installed.
    Provider/plugin registration must still succeed.
    """
    try:
        from bvillage.core.util_yaml import load_yaml
    except Exception:
        return

    locales = Path(__file__).parent / "locales"

    try:
        register_locale_catalog("de", load_yaml(locales / "de.yaml"))
    except Exception:
        pass

    try:
        register_locale_catalog("en", load_yaml(locales / "en.yaml"))
    except Exception:
        pass


def register() -> None:
    provider = LonghouseTypeProvider()

    register_provider_with_archetypes(
        provider,
        construction_grammars={
            "FW-LH-ND": "BOX_FRAME",
            "FW-LH-2S": "BOX_FRAME",
            "FW-LH-3S": "BOX_FRAME",
            "FW-LH-4S": "BOX_FRAME",
            "FW-GULF": "BOX_FRAME",
            "FW-HAUB": "BOX_FRAME",
            "FW-MITT": "BOX_FRAME",
            "FW-LH-EN": "BOX_FRAME",
        },
    )

    _try_register_locales()
