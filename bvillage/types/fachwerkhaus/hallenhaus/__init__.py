# bvillage/types/fachwerkhaus/hallenhaus/__init__.py

"""
bvillage.types.fachwerkhaus.hallenhaus
======================================

House Type: Fachwerkhaus – Hallenhaus
--------------------------------------

This module registers the house type provider
"fachwerkhaus.hallenhaus" in the central registry.

Responsibilities
----------------
- Provide a stable type_id.
- Implement generate(ctx) -> (structure, interior, openings).
- Register itself at import time.

Architecture
------------
- Domain engine: bvillage.domains.fachwerk
- Type-specific orchestration: planner.py
- Blender builder: domain-level

Units
-----
All geometry values are in meters.

Registration
------------
Registration happens at module import time.
The registry discovery system explicitly imports this package.

Design Note
-----------
This module must contain *no* heavy logic.
It only wires together planner + registry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple

from bvillage.core.registry import register_house_type, HouseTypeProvider
from .planner import generate_house

# ---------------------------------------------------------
# Provider Implementation
# ---------------------------------------------------------


@dataclass(slots=True)
class HallenhausProvider:
    """
    HouseTypeProvider implementation for Fachwerkhaus Hallenhaus.
    """

    type_id: str = "fachwerkhaus.hallenhaus"

    def generate(self, ctx: Any) -> Tuple[Any, Any, Any]:
        """
        Generate full house pipeline.

        Parameters
        ----------
        ctx :
            Execution context (policy, config, runtime options).

        Returns
        -------
        tuple
            (structure, interior, openings)

        Contract
        --------
        - structure: core model object (units: meters)
        - interior: interior planning result
        - openings: normalized opening definitions

        This function delegates to planner.generate_house().
        """
        return generate_house(ctx)


# ---------------------------------------------------------
# Registration
# ---------------------------------------------------------

_provider = HallenhausProvider()

register_house_type(_provider, origin=__name__)
