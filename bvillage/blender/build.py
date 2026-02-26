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

- Reads Fachwerk planning artifacts via bvillage.core.notes.get_domain_artifact()
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
from bvillage.core.notes import get_domain_artifact

# Domain builder: consumes explicit frameplan dict
from bvillage.domains.fachwerk.blender.build_frame import build_fachwerk_frame

logger = logging.getLogger(__name__)


def _require_fachwerk_frameplan(structure: StructurePlan) -> dict:
    """
    Load fachwerk.frameplan artifact via canonical schema.

    Transitional legacy aliases allowed (read-only):
      - legacy frameplan alias (flat key)
      - legacy qualified alias (fachwerk.frameplan)

    Raises
    ------
    RuntimeError if artifact is missing or invalid.
    """
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise RuntimeError("StructurePlan.notes missing or invalid.")

    frameplan = get_domain_artifact(
        notes,
        domain="fachwerk",
        artifact="frameplan",
        legacy_aliases=("frameplan", "fachwerk.frameplan"),
    )

    if frameplan is None:
        raise RuntimeError(
            "Missing required artifact: fachwerk.frameplan (canonical or legacy alias)."
        )
    if not isinstance(frameplan, dict):
        raise RuntimeError("fachwerk.frameplan must be a dict payload.")

    return frameplan


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
        Structural plan; must contain fachwerk.frameplan artifact for Fachwerk frame build.
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
    3) Build Fachwerk timber frame into Structure (artifact-driven).
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

    frameplan = _require_fachwerk_frameplan(structure)

    build_fachwerk_frame(
        ctx=ctx,
        structure=structure,
        frameplan=frameplan,
        root_collection=col_structure,
        clear_previous=clear_previous,
    )

    # ---- Openings props placeholder ----
    # (Optional future) gates/windows leaves/shutters as separate objects.
    # Keep this out until frameplan is stable to avoid visual clutter.

    # ---- Interior placeholder ----
    # (Future) floors, partitions, furniture based on InteriorPlan.

    return root
