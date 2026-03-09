# bvillage/domains/timber_frame/core/derive_roofplan_boxframe.py
from __future__ import annotations

from math import radians, tan
from typing import Any

from bvillage.core.errors import SchemaError

__all__ = ["derive_roofplan_boxframe"]


def _resolve_pitch_deg(resolved_policy: Any) -> float:
    default_pitch = 50.0

    if resolved_policy is None:
        return default_pitch

    if isinstance(resolved_policy, dict):
        for key in (
            "fachwerk.roof_pitch_deg",
            "roof_pitch_deg",
            "roof.pitch_deg",
        ):
            value = resolved_policy.get(key)
            if value is not None:
                try:
                    return float(value)
                except Exception:
                    return default_pitch

    for attr in (
        "roof_pitch_deg",
        "fachwerk_roof_pitch_deg",
    ):
        value = getattr(resolved_policy, attr, None)
        if value is not None:
            try:
                return float(value)
            except Exception:
                return default_pitch

    return default_pitch


def _resolve_kehl_frac(resolved_policy: Any) -> float:
    default_frac = 0.58

    if resolved_policy is None:
        return default_frac

    if isinstance(resolved_policy, dict):
        for key in (
            "fachwerk.kehl_frac",
            "roof.kehl_frac",
            "kehl_frac",
        ):
            value = resolved_policy.get(key)
            if value is not None:
                try:
                    frac = float(value)
                    return max(0.50, min(0.70, frac))
                except Exception:
                    return default_frac

    value = getattr(resolved_policy, "kehl_frac", None)
    if value is not None:
        try:
            frac = float(value)
            return max(0.50, min(0.70, frac))
        except Exception:
            return default_frac

    return default_frac


def _resolve_profiles(resolved_policy: Any) -> dict[str, tuple[float, float]]:
    profiles = {
        "ridge": (0.18, 0.22),
        "rafter": (0.10, 0.16),
        "collar": (0.12, 0.16),
    }

    if not isinstance(resolved_policy, dict):
        return profiles

    candidate = resolved_policy.get("roof.profiles")
    if not isinstance(candidate, dict):
        return profiles

    out = dict(profiles)
    for key in ("ridge", "rafter", "collar"):
        value = candidate.get(key)
        if isinstance(value, (list, tuple)) and len(value) == 2:
            try:
                out[key] = (float(value[0]), float(value[1]))
            except Exception:
                pass
    return out


def _extract_frame_x_positions(frameplan: dict[str, Any]) -> list[float]:
    frame_layout = frameplan.get("frame_layout")
    if not isinstance(frame_layout, dict):
        raise SchemaError("FramePlan.frame_layout missing/invalid for roof derivation")

    xs = frame_layout.get("x_frames")
    if not isinstance(xs, list) or len(xs) < 2:
        raise SchemaError("FramePlan.frame_layout.x_frames missing/invalid for roof derivation")

    return [float(x) for x in xs]


def _extract_half_width(frameplan: dict[str, Any]) -> float:
    basis = frameplan.get("basis")
    if not isinstance(basis, dict):
        raise SchemaError("FramePlan.basis missing/invalid for roof derivation")

    half_w = basis.get("halfW")
    if half_w is None:
        raise SchemaError("FramePlan.basis.halfW missing for roof derivation")

    return float(half_w)


def _extract_z_plate(frameplan: dict[str, Any]) -> float:
    basis = frameplan.get("basis")
    if not isinstance(basis, dict):
        raise SchemaError("FramePlan.basis missing/invalid for roof derivation")

    z_plate = basis.get("z_plate")
    if z_plate is None:
        raise SchemaError("FramePlan.basis.z_plate missing for roof derivation")

    return float(z_plate)


def _extract_y_rows(frameplan: dict[str, Any]) -> list[float]:
    frame_layout = frameplan.get("frame_layout")
    if not isinstance(frame_layout, dict):
        raise SchemaError("FramePlan.frame_layout missing/invalid for roof derivation")

    ys = frame_layout.get("y_rows")
    if not isinstance(ys, list) or len(ys) < 2:
        raise SchemaError("FramePlan.frame_layout.y_rows missing/invalid for roof derivation")

    return [float(y) for y in ys]


def derive_roofplan_boxframe(
    frameplan: dict[str, Any],
    *,
    resolved_policy: Any = None,
) -> dict[str, Any]:
    """
    Derive a dedicated RoofPlan from FramePlan + policy.

    HARD RULE:
    - roof structure is produced in domain logic
    - renderer must not derive rafters/collars/ridge from planning axes
    """
    xs = _extract_frame_x_positions(frameplan)
    _ = _extract_y_rows(frameplan)  # kept as an explicit contract dependency
    half_width = _extract_half_width(frameplan)
    z_plate = _extract_z_plate(frameplan)

    pitch_deg = _resolve_pitch_deg(resolved_policy)
    kehl_frac = _resolve_kehl_frac(resolved_policy)
    profiles = _resolve_profiles(resolved_policy)

    h = tan(radians(pitch_deg)) * half_width
    z_ridge = z_plate + h
    z_kehl = z_plate + kehl_frac * (z_ridge - z_plate)
    y_kehl = (z_kehl - z_plate) / tan(radians(pitch_deg))

    members = {
        "ridge": [],
        "rafters": [],
        "collar_ties": [],
    }

    members["ridge"].append(
        {
            "id": "RIDGE_01",
            "tid": "roof.ridge",
            "p0": [float(xs[0]), 0.0, z_ridge],
            "p1": [float(xs[-1]), 0.0, z_ridge],
            "profile": {
                "width": profiles["ridge"][0],
                "depth": profiles["ridge"][1],
            },
        }
    )

    for i in range(len(xs) - 1):
        xmid = 0.5 * (float(xs[i]) + float(xs[i + 1]))

        members["rafters"].append(
            {
                "id": f"RAFTER_L_{i:02d}",
                "tid": "roof.rafter.left",
                "p0": [xmid, -half_width, z_plate],
                "p1": [xmid, 0.0, z_ridge],
                "profile": {
                    "width": profiles["rafter"][0],
                    "depth": profiles["rafter"][1],
                },
            }
        )

        members["rafters"].append(
            {
                "id": f"RAFTER_R_{i:02d}",
                "tid": "roof.rafter.right",
                "p0": [xmid, +half_width, z_plate],
                "p1": [xmid, 0.0, z_ridge],
                "profile": {
                    "width": profiles["rafter"][0],
                    "depth": profiles["rafter"][1],
                },
            }
        )

        members["collar_ties"].append(
            {
                "id": f"COLLAR_{i:02d}",
                "tid": "roof.collar_tie",
                "p0": [xmid, -y_kehl, z_kehl],
                "p1": [xmid, +y_kehl, z_kehl],
                "profile": {
                    "width": profiles["collar"][0],
                    "depth": profiles["collar"][1],
                },
            }
        )

    return {
        "schema_version": "0.1.0",
        "coordinate_system": "BVILLAGE_RIGHT_HANDED_Z_UP",
        "roof_type": "gable_rafter_roof",
        "basis": {
            "x_frames": xs,
            "half_width": half_width,
            "z_plate": z_plate,
            "pitch_deg": pitch_deg,
            "z_ridge": z_ridge,
            "z_kehl": z_kehl,
            "y_kehl": y_kehl,
            "kehl_frac": kehl_frac,
        },
        "members": members,
    }
