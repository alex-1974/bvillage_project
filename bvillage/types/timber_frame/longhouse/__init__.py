# bvillage/types/timber_frame/longhouse/__init__.py
from __future__ import annotations

from bvillage.core.dispatch_registry import register_provider_with_archetypes
from .provider import LonghouseTypeProvider

__all__ = ["register", "SUPPORTED_ARCHETYPES", "LonghouseTypeProvider"]


SUPPORTED_ARCHETYPES: dict[str, str] = {
    "FW-LH-ND": "BOX_FRAME",
}


def register() -> None:
    """
    Register supported longhouse archetypes.

    Architecture
    ------------
    Type plugins register themselves.
    Core must not hardcode archetype knowledge.
    """
    provider = LonghouseTypeProvider()

    register_provider_with_archetypes(
        provider,
        construction_grammars=SUPPORTED_ARCHETYPES,
    )
