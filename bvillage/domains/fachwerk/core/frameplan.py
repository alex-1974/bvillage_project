# bvillage/domains/fachwerk/core/frameplan.py

"""
bvillage.domains.fachwerk.core.frameplan
=======================================

Build a Fachwerk frameplan artifact.

This revision centralizes eps/tolerances via bvillage.core.geom_eps and keeps
behavior deterministic and stable.

Units: meters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Tuple

from bvillage.core.geom_eps import EPS_MERGE
from bvillage.core.model import StructurePlan
from bvillage.domains.fachwerk.core.openings_norm import (
    OpeningFinal,
    normalize_openings_from_plan,
)
from bvillage.domains.fachwerk.core.axes_u import compute_vertical_axes
from bvillage.domains.fachwerk.core.axes_z import compute_z_axes
from bvillage.domains.fachwerk.core.wall_tags import compute_wall_tags, suggest_front_wall


@dataclass(frozen=True, slots=True)
class FramePolicy:
    """
    Fachwerk engine policy parameters.

    Units: meters.
    """
    b_max: float
    default_jamb_t: float = 0.20
    horizontal_axes_style: List[float] = None  # type: ignore[assignment]
    z_merge_tol: float = EPS_MERGE
    z_band_min: float = 0.15
    z_band_target_min: float = 0.25
    width_type: Literal["axis", "clear"] = "axis"

    def __post_init__(self) -> None:
        if self.horizontal_axes_style is None:
            object.__setattr__(self, "horizontal_axes_style", [0.0, 0.9, 1.6, 2.2, 2.58])
        # Ensure merge tol is not tighter than global default unless explicitly desired.
        if float(self.z_merge_tol) < EPS_MERGE:
            object.__setattr__(self, "z_merge_tol", EPS_MERGE)


@dataclass(frozen=True, slots=True)
class FramePlan:
    """Completed Fachwerk frameplan artifact (units: meters)."""
    L: float
    W: float
    H_e: float
    z0: float

    openings_final: List[OpeningFinal]
    vertical_axes: Dict[str, Dict[str, List[float]]]
    z_axes: List[float]
    z_clusters: List[List[float]]
    z_repair_log: List[str]
    wall_tags: Dict[str, Any]
    front_wall: str


def _infer_wall_height(structure: StructurePlan) -> Tuple[float, float]:
    """
    Infer (z0, H_e) from the first wall segment with z_range.

    Fallback if structure does not provide walls: (0.0, 2.5)
    """
    walls = getattr(structure, "walls", ())
    for w in walls:
        zr = getattr(w, "z_range", None)
        if isinstance(zr, tuple) and len(zr) == 2:
            z0 = float(zr[0])
            H_e = float(zr[1])
            if H_e < z0:
                z0, H_e = H_e, z0
            return z0, H_e
    return 0.0, 2.5


def build_frameplan(*, structure: StructurePlan, openings: Any, policy: FramePolicy) -> FramePlan:
    """
    Build frameplan artifact for the given structure and openings.

    Returns
    -------
    FramePlan
    """
    L = float(structure.footprint.length)
    W = float(structure.footprint.width)

    z0, H_e = _infer_wall_height(structure)

    openings_final = normalize_openings_from_plan(
        openings,
        default_jamb_t=float(policy.default_jamb_t),
        width_type=policy.width_type,
    )

    vertical_axes = compute_vertical_axes(
        L=L,
        W=W,
        b_max=float(policy.b_max),
        openings=list(openings_final),
    )

    z_axes, z_clusters, z_repair_log = compute_z_axes(
        z0=z0,
        H_e=H_e,
        horizontal_axes_style=list(policy.horizontal_axes_style),
        z_merge_tol=float(policy.z_merge_tol),
        z_band_min=float(policy.z_band_min),
        z_band_target_min=float(policy.z_band_target_min),
        openings=list(openings_final),
    )

    wall_tags = compute_wall_tags(openings_final)
    front_wall = suggest_front_wall(wall_tags)

    return FramePlan(
        L=L,
        W=W,
        H_e=H_e,
        z0=z0,
        openings_final=list(openings_final),
        vertical_axes=vertical_axes,
        z_axes=z_axes,
        z_clusters=z_clusters,
        z_repair_log=z_repair_log,
        wall_tags=wall_tags,
        front_wall=front_wall,
    )


def frameplan_to_dict(fp: FramePlan) -> Dict[str, Any]:
    """Convert FramePlan to a JSON-like dict for notes storage (stable schema)."""
    return {
        "dims": {"L": fp.L, "W": fp.W, "H_e": fp.H_e, "z0": fp.z0},
        "openings": [
            {
                "name": o.name,
                "type": o.typ,
                "wall": o.wall,
                "u0": o.u0,
                "u1": o.u1,
                "u_center": o.u_center,
                "width_axis": o.width_axis,
                "width_clear": o.width_clear,
                "z0": o.z0,
                "z1": o.z1,
                "jamb_t": o.jamb_t,
            }
            for o in fp.openings_final
        ],
        "axes_u": fp.vertical_axes,
        "axes_z": fp.z_axes,
        "z_repair_log": list(fp.z_repair_log),
        "wall_tags": fp.wall_tags,
        "front_wall": fp.front_wall,
    }


def frameplan_report(fp: FramePlan) -> str:
    """Human-readable planner report."""
    lines: List[str] = []
    lines.append("========== PLANNER REPORT ==========")
    lines.append(f"[Dims] L={fp.L:.3f} W={fp.W:.3f} H_e={fp.H_e:.3f} z0={fp.z0:.3f}")
    lines.append("[Z Axes] " + ", ".join(f"{z:.3f}" for z in fp.z_axes))

    if fp.z_repair_log:
        lines.append("[Z Repair Log]")
        for msg in fp.z_repair_log:
            lines.append(f"  - {msg}")

    lines.append(f"[Openings Final] n={len(fp.openings_final)}")
    for o in fp.openings_final:
        lines.append(
            f"  {o.name:>4} {o.typ:<6} wall={o.wall} "
            f"u_axis=[{o.u0:+.3f},{o.u1:+.3f}] (axis={o.width_axis:.3f} clear={o.width_clear:.3f}) "
            f"z=[{o.z0:.3f},{o.z1:.3f}]"
        )

    lines.append("[Axes Summary]")
    for wall in ("N", "S", "E", "W"):
        w = fp.vertical_axes[wall]
        lines.append(
            f"  Wall {wall}: primary={len(w['primary'])} opening={len(w['opening'])} "
            f"secondary={len(w['secondary'])} all={len(w['all'])}"
        )

    lines.append(f"[Front Wall] {fp.front_wall}")
    return "\n".join(lines)
