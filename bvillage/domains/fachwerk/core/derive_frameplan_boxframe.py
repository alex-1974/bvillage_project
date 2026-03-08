# bvillage/domains/fachwerk/core/derive_frameplan_boxframe.py
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from bvillage.core.errors import SchemaError
from bvillage.core.model import StructurePlan
from bvillage.core.ontology.structural_terms import (
    POST_OPENING_JAMB,
    BEAM_OPENING_LINTEL,
    BRACE_KNEE,
)

from bvillage.types.fachwerkhaus.hallenhaus.contracts.schema_frameplan_langhaus

__all__ = ["derive_frameplan_boxframe"]


def derive_frameplan_boxframe(
    ctx: Any,
    structure: StructurePlan,
) -> FramePlanFachwerk:
    """
    Derive a members-first Fachwerk FramePlan from StructurePlan.

    Architecture
    ------------
    Domain layer:
        StructurePlan → FramePlan

    This function must remain side-effect free.
    """

    xs = _extract_x_frames(structure)
    row_ys = _extract_row_positions(structure)
    frame_roles = _extract_frame_roles(structure)

    z0, z_plate = _extract_vertical_basis(structure)

    posts: List[Dict[str, Any]] = []
    rails: List[Dict[str, Any]] = []
    braces: List[Dict[str, Any]] = []

    # --------------------------------------------------
    # Posts
    # --------------------------------------------------

    for i, x in enumerate(xs):
        role = frame_roles[i]

        posts.append(
            {
                "id": f"P_{i}_S",
                "tid": "post.primary",
                "p0": (x, row_ys[0], z0),
                "p1": (x, row_ys[0], z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )

        posts.append(
            {
                "id": f"P_{i}_H",
                "tid": "post.hall",
                "p0": (x, row_ys[1], z0),
                "p1": (x, row_ys[1], z_plate),
                "tags": ("ROW_HALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )

        posts.append(
            {
                "id": f"P_{i}_N",
                "tid": "post.primary",
                "p0": (x, row_ys[2], z0),
                "p1": (x, row_ys[2], z_plate),
                "tags": ("ROW_WALL", f"FRAME_{i}", f"FrameRole.{role}"),
            }
        )

    # --------------------------------------------------
    # Plates
    # --------------------------------------------------

    for i in range(len(xs) - 1):
        x0 = xs[i]
        x1 = xs[i + 1]

        rails.append(
            {
                "id": f"PL_S_{i}",
                "tid": "beam.plate",
                "p0": (x0, row_ys[0], z_plate),
                "p1": (x1, row_ys[0], z_plate),
                "tags": ("WALL_S",),
            }
        )

        rails.append(
            {
                "id": f"PL_N_{i}",
                "tid": "beam.plate",
                "p0": (x0, row_ys[2], z_plate),
                "p1": (x1, row_ys[2], z_plate),
                "tags": ("WALL_N",),
            }
        )

    # --------------------------------------------------
    # Braces
    # --------------------------------------------------

    bid = 0

    for i in range(len(xs) - 1):
        x0 = xs[i]
        x1 = xs[i + 1]

        braces.append(
            {
                "id": f"BR_{bid}",
                "tid": BRACE_KNEE,
                "p0": (x0, row_ys[0], z_plate * 0.3),
                "p1": (x1, row_ys[0], z_plate * 0.8),
                "tags": ("WALL_S",),
            }
        )

        bid += 1

    # --------------------------------------------------
    # Gate
    # --------------------------------------------------

    gate_x = max(xs)
    gate_width = 3.0
    gate_half = gate_width / 2
    gate_height = 2.2

    posts.append(
        {
            "id": "OJ_GATE_L",
            "tid": POST_OPENING_JAMB,
            "p0": (gate_x, -gate_half, z0),
            "p1": (gate_x, -gate_half, gate_height),
            "tags": ("OPENING_GATE",),
        }
    )

    posts.append(
        {
            "id": "OJ_GATE_R",
            "tid": POST_OPENING_JAMB,
            "p0": (gate_x, gate_half, z0),
            "p1": (gate_x, gate_half, gate_height),
            "tags": ("OPENING_GATE",),
        }
    )

    rails.append(
        {
            "id": "OL_GATE",
            "tid": BEAM_OPENING_LINTEL,
            "p0": (gate_x, -gate_half, gate_height),
            "p1": (gate_x, gate_half, gate_height),
            "tags": ("OPENING_GATE",),
        }
    )

    # --------------------------------------------------
    # FrameLayout
    # --------------------------------------------------

    frame_layout = {
        "x_frames": list(xs),
        "y_rows": list(row_ys),
        "frame_roles": list(frame_roles),
    }

    frameplan: FramePlanFachwerk = {
        "schema_version": SCHEMA_VERSION_FACHWERK,
        "coordinate_system": {
            "origin": "building_center_ground",
            "axes": {
                "x": "longitudinal_forward",
                "y": "right_when_facing_positive_x",
                "z": "up",
            },
            "units": "meters",
        },
        "basis": {
            "z0": z0,
            "z_plate": z_plate,
        },
        "frame_layout": frame_layout,
        "members": {
            "posts": posts,
            "rails": rails,
            "braces": braces,
            "infills": [],
        },
        "openings": [],
        "notes": {
            "gate": {
                "placement": "gable_end",
                "wall": "W_E_0",
            }
        },
    }

    return frameplan


# --------------------------------------------------
# Helpers
# --------------------------------------------------


def _extract_x_frames(structure: StructurePlan) -> Tuple[float, ...]:
    xs = tuple(float(x) for x in structure.grid.axes_u)

    if len(xs) < 2:
        raise SchemaError("BOX_FRAME requires ≥2 frame axes")

    return xs


def _extract_row_positions(structure: StructurePlan) -> Tuple[float, float, float]:
    ys = tuple(sorted(float(y) for y in structure.grid.axes_v))

    if len(ys) != 3:
        raise SchemaError("Hallenhaus requires exactly 3 row positions")

    return ys


def _extract_frame_roles(structure: StructurePlan) -> Tuple[str, ...]:
    roles = []

    for frame in structure.frames:
        role = None

        for tag in frame.tags:
            if tag.startswith("FrameRole."):
                role = tag.split(".", 1)[1]
                break

        if role is None:
            raise SchemaError(f"Frame {frame.id} missing role")

        roles.append(role)

    return tuple(roles)


def _extract_vertical_basis(structure: StructurePlan) -> Tuple[float, float]:
    if not structure.walls:
        raise SchemaError("StructurePlan missing walls")

    z0 = min(w.z_range[0] for w in structure.walls)
    z1 = max(w.z_range[1] for w in structure.walls)

    return float(z0), float(z1)
