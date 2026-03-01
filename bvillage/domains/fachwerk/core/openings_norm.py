# bvillage/domains/fachwerk/core/openings_norm.py

"""
bvillage.domains.fachwerk.core.openings_norm
============================================

Normalize house-type openings into a Fachwerk-engine friendly representation.

See earlier version for detailed rationale; this revision centralizes eps/tolerances
via bvillage.core.geom_eps.

Units: meters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Literal

from bvillage.core.geom_eps import EPS_EQ, EPS_INSIDE

WidthType = Literal["axis", "clear"]


@dataclass(frozen=True, slots=True)
class OpeningFinal:
    """
    Normalized opening representation for the Fachwerk engine.

    Units: meters.
    """
    name: str
    typ: str
    wall: str
    u0: float
    u1: float
    u_center: float
    width_range: float
    width_clear: float
    z0: float
    z1: float
    jamb_thickness: float


def wall_side_from_id(wall_id: str) -> str:
    """
    Map wall segment IDs to wall sides.

    Expected:
    - "W_N_*" -> "N"
    - "W_S_*" -> "S"
    - "W_E_*" -> "E"
    - "W_W_*" -> "W"
    """
    if not isinstance(wall_id, str) or len(wall_id) < 3:
        raise ValueError(f"Invalid wall_id: {wall_id!r}")

    if wall_id.startswith("W_N_"):
        return "N"
    if wall_id.startswith("W_S_"):
        return "S"
    if wall_id.startswith("W_E_"):
        return "E"
    if wall_id.startswith("W_W_"):
        return "W"

    raise ValueError(f"Cannot derive wall side from wall_id={wall_id!r}. Expected 'W_[NSEW]_...'.")


def normalize_openings_from_plan(
    openings_plan: Any,
    *,
    default_jamb_thickness: float,
    width_type: WidthType = "axis",
) -> list[OpeningFinal]:
    """
    Normalize a house-type OpeningsPlan into a list of OpeningFinal.

    Parameters
    ----------
    openings_plan:
        Object with `.openings` iterable.
    default_jamb_thickness:
        Default jamb thickness (meters).
    width_type:
        - "axis": u_range is axis width; clear = axis - jamb_thickness
        - "clear": u_range is clear width; axis = clear + jamb_thickness

    Returns
    -------
    list[OpeningFinal]
        Sorted by (wall, u_center, name) deterministically.
    """
    openings: Iterable[Any] = getattr(openings_plan, "openings", ())
    jamb_thickness = float(default_jamb_thickness)

    finals: list[OpeningFinal] = []
    for op in openings:
        name = str(getattr(op, "id", ""))
        typ = str(getattr(op, "type", getattr(op, "typ", "")))

        wall_id = getattr(op, "wall_id", None)
        if not isinstance(wall_id, str):
            raise ValueError(f"Opening {name!r} missing wall_id.")
        wall = wall_side_from_id(wall_id)

        u_range = getattr(op, "u_range", None)
        z_range = getattr(op, "z_range", None)
        if not (isinstance(u_range, tuple) and len(u_range) == 2):
            raise ValueError(f"Opening {name!r} invalid u_range={u_range!r}")
        if not (isinstance(z_range, tuple) and len(z_range) == 2):
            raise ValueError(f"Opening {name!r} invalid z_range={z_range!r}")

        u0 = float(u_range[0])
        u1 = float(u_range[1])
        if u1 < u0:
            u0, u1 = u1, u0

        z0 = float(z_range[0])
        z1 = float(z_range[1])
        if z1 < z0:
            z0, z1 = z1, z0

        width_in = u1 - u0
        if width_in <= EPS_EQ:
            raise ValueError(f"Opening {name!r} has non-positive width_in={width_in} (u0={u0}, u1={u1}).")

        if width_type == "axis":
            width_range = width_in
            width_clear = width_range - jamb_thickness
            if width_clear <= EPS_EQ:
                raise ValueError(
                    f"Opening {name!r} clear width <= 0. axis={width_range}, jamb_thickness={jamb_thickness}."
                )
            u0n, u1n = u0, u1

        elif width_type == "clear":
            width_clear = width_in
            width_range = width_clear + jamb_thickness
            if width_range <= EPS_EQ:
                raise ValueError(
                    f"Opening {name!r} axis width <= 0. clear={width_clear}, jamb_thickness={jamb_thickness}."
                )
            # Expand around center by jamb/2 on each side
            u_center = (u0 + u1) / 2.0
            half_axis = width_range / 2.0
            u0n = u_center - half_axis
            u1n = u_center + half_axis

        else:
            raise ValueError(f"Unknown width_type={width_type!r}. Expected 'axis' or 'clear'.")

        # Avoid micro inversions after float ops
        if u1n < u0n - EPS_INSIDE:
            raise ValueError(f"Opening {name!r} produced inverted u interval after normalization.")
        if z1 < z0 - EPS_INSIDE:
            raise ValueError(f"Opening {name!r} produced inverted z interval after normalization.")

        u_center = (u0n + u1n) / 2.0

        finals.append(
            OpeningFinal(
                name=name,
                typ=typ,
                wall=wall,
                u0=u0n,
                u1=u1n,
                u_center=u_center,
                width_range=width_range,
                width_clear=width_clear,
                z0=z0,
                z1=z1,
                jamb_thickness=jamb_thickness,
            )
        )

    finals.sort(key=lambda o: (o.wall, o.u_center, o.name))
    return finals
