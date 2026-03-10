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
render_house(ctx, structure, interior, openings, clear_previous=True) -> bpy.types.Collection

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

from bvillage.domains.timber_frame.blender.build_frame import build_fachwerk_frame_from_structure_notes
from bvillage.domains.timber_frame.blender.roof import build_roof_from_plan

logger = logging.getLogger(__name__)


def _require_fachwerk_frameplan(structure: StructurePlan) -> dict:
    """
    Load fachwerk.frameplan artifact via canonical schema.

    Raises
    ------
    RuntimeError if artifact is missing or invalid.
    """
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise RuntimeError("StructurePlan.notes missing or invalid.")

    frameplan = get_domain_artifact(
        structure.notes,
        domain="fachwerk",
        artifact="frameplan",
    )

    if frameplan is None:
        raise RuntimeError("Missing required artifact: fachwerk.frameplan.")

    if not isinstance(frameplan, dict):
        raise RuntimeError("fachwerk.frameplan must be a dict payload.")

    return frameplan


def _require_fachwerk_roofplan(structure: StructurePlan) -> dict:
    """
    Load fachwerk.roofplan artifact.

    Raises
    ------
    RuntimeError if artifact is missing or invalid.
    """
    notes = getattr(structure, "notes", None)
    if not isinstance(notes, dict):
        raise RuntimeError("StructurePlan.notes missing or invalid.")

    roofplan = get_domain_artifact(
        structure.notes,
        domain="fachwerk",
        artifact="roofplan",
    )

    if roofplan is None:
        raise RuntimeError("Missing required artifact: fachwerk.roofplan.")

    if not isinstance(roofplan, dict):
        raise RuntimeError("fachwerk.roofplan must be a dict payload.")

    return roofplan


def render_house(
    ctx: Context,
    structure: StructurePlan,
    interior: InteriorPlan,
    openings: OpeningsPlan,
    *,
    clear_previous: bool = True,
) -> bpy.types.Collection:
    """
    Build the house in the Blender scene.
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

    logger.info("Blender build: Fachwerk frame (House=%s)", house_root_name)

    _ = _require_fachwerk_frameplan(structure)

    root_collection = bpy.context.scene.collection

    build_fachwerk_frame_from_structure_notes(
        ctx=ctx,
        structure=structure,
        root_collection=root_collection,
        clear_previous=clear_previous,
    )

    logger.info("Blender build: roof")

    roofplan = _require_fachwerk_roofplan(structure)

    build_roof_from_plan(
        roofplan=roofplan,
        col_roof=col_structure,
    )

    return root
