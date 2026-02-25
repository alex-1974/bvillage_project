# bvillage/blender/build.py

"""
bvillage.blender.build
=====================

Purpose
-------
Blender-side scene build orchestration.

This module is intentionally *domain-lean*:
- It consumes planning artifacts (StructurePlan, InteriorPlan, OpeningsPlan).
- It builds Blender objects by delegating to domain builders.
- It should not import type-specific planners or generators.

Contracts
---------
build_house(ctx, structure, interior, openings, clear_previous=True) -> bpy.types.Collection

- Reads `structure.notes["frameplan"]` (compat key) produced by the Fachwerk domain.
- Does not mutate planning objects.

Units
-----
All plan geometry is in meters.

Notes
-----
This file may import `bpy` and must only be executed inside Blender.
"""

from __future__ import annotations

import logging
import bpy

from bvillage.core.model import Context, StructurePlan, InteriorPlan, OpeningsPlan
from bvillage.blender.utils import ensure_collection, clear_collection

# Domain builder: consumes structure.notes["frameplan"] dict
from bvillage.domains.fachwerk.blender.build_frame import build_fachwerk_frame_from_structure_notes

logger = logging.getLogger(__name__)


def build_house(
    ctx: Context,
    structure: StructurePlan,
    interior: InteriorPlan,
    openings: OpeningsPlan,
    *,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    """
    Build the house in the Blender scene.

    Parameters
    ----------
    ctx:
        Execution context (used mainly for naming / seeding).
    structure:
        Structural plan; must contain `notes["frameplan"]` if Fachwerk frame is desired.
    interior:
        Interior plan (currently not built into geometry here; placeholder).
    openings:
        Openings plan (currently not built into geometry here; placeholder).
    clear_previous:
        If True, clears the per-house sub-collections before building.

    Returns
    -------
    bpy.types.Collection
        Root collection for the house build.

    Current build steps
    -------------------
    1) Create (or reuse) House_<seed> root collection.
    2) Create sub-collections: Structure / Interior / Openings.
    3) Build Fachwerk timber frame into Structure/FachwerkFrame.
    4) Interior & opening-props are intentionally deferred until frame correctness is locked.

    Raises
    ------
    RuntimeError
        If required plan artifacts are missing (e.g. frameplan not attached).
    """
    house_root_name = f"House_{getattr(ctx, 'seed', 'NA')}"
    root = ensure_collection(house_root_name, parent=None)

    col_structure = ensure_collection("Structure", parent=root)
    col_interior = ensure_collection("Interior", parent=root)
    col_openings = ensure_collection("Openings", parent=root)

    if clear_previous:
        clear_collection(col_structure)
        clear_collection(col_interior)
        clear_collection(col_openings)

    # ---- Structure: Fachwerk frame ----
    logger.info("Blender build: Fachwerk frame (House=%s)", house_root_name)
    build_fachwerk_frame_from_structure_notes(
        structure=structure,
        root_collection=col_structure,
        clear_previous=False,
    )

    # ---- Openings props placeholder ----
    # (Optional future) gates/windows leaves/shutters as separate objects.
    # Keep this out until frameplan is stable to avoid visual clutter.

    # ---- Interior placeholder ----
    # (Future) floors, partitions, furniture based on InteriorPlan.

    return root
