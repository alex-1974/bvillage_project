"""
Timber-frame domain plugin bootstrap.

Registers the Foreman responsible for timber-frame construction grammar.
"""

from bvillage.core.foreman.plan_dispatch import register_foreman_for_grammar
from bvillage.domains.timber_frame.foreman.box_frame_foreman import BoxFrameForeman


def register():

    register_foreman_for_grammar(
        "BOX_FRAME",
        BoxFrameForeman(),
    )
