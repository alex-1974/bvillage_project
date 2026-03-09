# bvillage/types/timber_frame/longhouse/__init__.py
from __future__ import annotations

from pathlib import Path

from bvillage.core.schema_i18n import register_locale_catalog
from bvillage.core.util_yaml import load_yaml
from bvillage.foreman.plan_dispatch import register_provider_with_archetypes

from .provider import LonghouseTypeProvider

__all__ = ["LonghouseTypeProvider"]


_provider = LonghouseTypeProvider()

register_provider_with_archetypes(
    _provider,
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

_locales = Path(__file__).parent / "locales"

register_locale_catalog("de", load_yaml(_locales / "de.yaml"))
register_locale_catalog("en", load_yaml(_locales / "en.yaml"))
