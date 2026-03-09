from __future__ import annotations

from bvillage.core.dispatch_registry import register_foreman_for_grammar
from bvillage.domains.timber_frame.foreman.boxframe_foreman import BoxFrameForeman

__all__ = ["register"]


def register() -> None:
    register_foreman_for_grammar(
        "BOX_FRAME",
        BoxFrameForeman(),
    )
