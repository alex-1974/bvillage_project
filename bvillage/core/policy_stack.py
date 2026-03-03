# bvillage/core/policy_stack.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Tuple

from .model import Context
from .policy_types import (
    ResolvedPolicy,
    ConstraintSpec,
    RangeHardSpec,
    RangeSoftSpec,
    FachwerkPolicySpec,
)

# ============================================================
# Errors
# ============================================================


class PolicyResolutionError(RuntimeError):
    pass


# ============================================================
# Trace
# ============================================================


@dataclass(frozen=True, slots=True)
class TraceOp:
    key: str
    value: Any


@dataclass(frozen=True, slots=True)
class TraceLayer:
    layer_id: str
    ops: tuple[TraceOp, ...]


@dataclass(frozen=True, slots=True)
class ResolutionTrace:
    schema: int
    layers: tuple[TraceLayer, ...]


# ============================================================
# Schema & Registries
# ============================================================

_POLICY_SCHEMA_VERSION = 4

_EPOCH_ALIASES = {
    "E1": "early_medieval",
    "E2": "high_medieval",
    "E3": "late_medieval",
}

_ALLOWED_EPOCHS = {"early_medieval", "high_medieval", "late_medieval"}
_ALLOWED_SETTLEMENTS = {"rural", "village", "town"}

_ALLOWED_HOUSE_TYPES = {"fachwerkhaus.hallenhaus"}

_ALLOWED_CONSTRAINT_KEYS: dict[str, set[str]] = {
    "fachwerkhaus.hallenhaus": {"brustriegel_z", "gefach_width_target"},
}

_REQUIRED_CONSTRAINT_KEYS = _ALLOWED_CONSTRAINT_KEYS


# ============================================================
# Helpers
# ============================================================


def _normalize_epoch(epoch_raw: str) -> str:
    epoch = _EPOCH_ALIASES.get(epoch_raw, epoch_raw)
    if epoch not in _ALLOWED_EPOCHS:
        raise PolicyResolutionError(f"Unsupported epoch_band: {epoch_raw}")
    return epoch


def _require_house_type(ctx: Context) -> str:
    ht = ctx.house_type
    if ht not in _ALLOWED_HOUSE_TYPES:
        raise PolicyResolutionError(f"Unsupported house_type: {ht}")
    return ht


def _require_settlement(ctx: Context) -> str:
    st = ctx.settlement_type
    if st not in _ALLOWED_SETTLEMENTS:
        raise PolicyResolutionError(f"Unsupported settlement_type: {st}")
    return st


def _trace(layer_id: str, ops: Iterable[Tuple[str, Any]]) -> TraceLayer:
    return TraceLayer(
        layer_id=layer_id,
        ops=tuple(TraceOp(k, v) for k, v in sorted(ops, key=lambda x: x[0])),
    )


def _assert_allowed(name: str, keys, allowed):
    unknown = set(keys) - set(allowed)
    if unknown:
        raise PolicyResolutionError(f"{name}: unknown keys {sorted(unknown)}")


def _clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _round2(x: float) -> float:
    return round(float(x), 3)


# ============================================================
# Layer Builders
# ============================================================


def _baseline_layer() -> tuple[FachwerkPolicySpec, dict[str, ConstraintSpec], TraceLayer]:
    """
    Baseline is the "neutral, plausible" starting point.
    Type/epoch/settlement/wealth layers will refine these.
    """
    fw = FachwerkPolicySpec(
        binder_max=1.60,
        # everything else inherits defaults from policy_types.FachwerkPolicySpec
        # (mirrors FramePolicy defaults + renderer-facing defaults)
    )

    return (
        fw,
        {},
        _trace(
            "BaselinePolicy",
            [
                ("fachwerk.binder_max", fw.binder_max),
                ("fachwerk.default_jamb_thickness", fw.default_jamb_thickness),
                ("fachwerk.roof_pitch_deg", fw.roof_pitch_deg),
                ("fachwerk.post_section", fw.post_section),
                ("fachwerk.braces_enable", fw.braces_enable),
                ("fachwerk.target_gefach_width", fw.target_gefach_width),
                ("fachwerk.target_gefach_jitter", fw.target_gefach_jitter),
            ],
        ),
    )


def _epoch_layer(epoch: str, fw: FachwerkPolicySpec) -> tuple[FachwerkPolicySpec, TraceLayer]:
    """
    Epoch affects typical roof pitches, some section choices, etc.
    Values here are a *parametric model* (not a claim of historical truth).
    """
    pitch = float(fw.roof_pitch_deg)
    post_w, post_d = fw.post_section

    if epoch == "early_medieval":
        pitch += 3.0
        post_w += 0.01
        post_d += 0.01
    elif epoch == "high_medieval":
        pass
    elif epoch == "late_medieval":
        pitch -= 1.0
        post_w += 0.005
        post_d += 0.005
    else:
        raise PolicyResolutionError(f"Unsupported epoch_band: {epoch}")

    pitch = max(35.0, min(70.0, pitch))
    post_w = max(0.14, min(0.30, post_w))
    post_d = max(0.14, min(0.30, post_d))

    out = FachwerkPolicySpec(
        binder_max=fw.binder_max,
        default_jamb_thickness=fw.default_jamb_thickness,
        post_section_width=fw.post_section_width,
        post_section_depth=fw.post_section_depth,
        plate_section_width=fw.plate_section_width,
        plate_section_depth=fw.plate_section_depth,
        opening_jamb_width=fw.opening_jamb_width,
        opening_jamb_depth=fw.opening_jamb_depth,
        braces_enable=fw.braces_enable,
        brace_section_width=fw.brace_section_width,
        brace_section_depth=fw.brace_section_depth,
        brace_min_cell_width=fw.brace_min_cell_width,
        brace_min_cell_height=fw.brace_min_cell_height,
        target_gefach_width=fw.target_gefach_width,
        target_gefach_jitter=fw.target_gefach_jitter,
        z_merge_tol=fw.z_merge_tol,
        roof_pitch_deg=pitch,
        post_section=(post_w, post_d),
    )

    return out, _trace(
        f"EpochPolicy:{epoch}",
        [
            ("fachwerk.roof_pitch_deg", out.roof_pitch_deg),
            ("fachwerk.post_section", out.post_section),
        ],
    )


def _settlement_layer(settlement: str, fw: FachwerkPolicySpec) -> tuple[FachwerkPolicySpec, TraceLayer]:
    """
    Settlement can affect the structural rhythm and ornament/brace density assumptions.
    Keep it mild for now.
    """
    binder = float(fw.binder_max)
    braces_enable = bool(fw.braces_enable)

    if settlement == "rural":
        pass
    elif settlement == "village":
        binder += 0.01
    elif settlement == "town":
        binder += 0.02
        braces_enable = True
    else:
        raise PolicyResolutionError(f"Unsupported settlement_type: {settlement}")

    binder = max(1.20, min(2.40, binder))

    out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fw.default_jamb_thickness,
        post_section_width=fw.post_section_width,
        post_section_depth=fw.post_section_depth,
        plate_section_width=fw.plate_section_width,
        plate_section_depth=fw.plate_section_depth,
        opening_jamb_width=fw.opening_jamb_width,
        opening_jamb_depth=fw.opening_jamb_depth,
        braces_enable=braces_enable,
        brace_section_width=fw.brace_section_width,
        brace_section_depth=fw.brace_section_depth,
        brace_min_cell_width=fw.brace_min_cell_width,
        brace_min_cell_height=fw.brace_min_cell_height,
        target_gefach_width=fw.target_gefach_width,
        target_gefach_jitter=fw.target_gefach_jitter,
        z_merge_tol=fw.z_merge_tol,
        roof_pitch_deg=fw.roof_pitch_deg,
        post_section=fw.post_section,
    )

    return out, _trace(
        f"SettlementPolicy:{settlement}",
        [
            ("fachwerk.binder_max", out.binder_max),
            ("fachwerk.braces_enable", out.braces_enable),
        ],
    )


def _wealth_layer(wealth: float, fw: FachwerkPolicySpec) -> tuple[FachwerkPolicySpec, TraceLayer]:
    """
    Wealth affects section sizes and sometimes pitch/regularity assumptions.
    """
    w = _clamp01(wealth)

    binder = float(fw.binder_max) + 0.10 * (w - 0.5)

    # beef up posts slightly with wealth
    post_w, post_d = fw.post_section
    post_w = post_w + 0.02 * (w - 0.5)
    post_d = post_d + 0.02 * (w - 0.5)

    # roof pitch: richer -> can afford steeper/complex roofs (tiny effect)
    pitch = float(fw.roof_pitch_deg) + 2.0 * (w - 0.5)

    binder = max(1.20, min(2.40, binder))
    post_w = max(0.14, min(0.30, post_w))
    post_d = max(0.14, min(0.30, post_d))
    pitch = max(35.0, min(70.0, pitch))

    out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fw.default_jamb_thickness,
        post_section_width=fw.post_section_width,
        post_section_depth=fw.post_section_depth,
        plate_section_width=fw.plate_section_width,
        plate_section_depth=fw.plate_section_depth,
        opening_jamb_width=fw.opening_jamb_width,
        opening_jamb_depth=fw.opening_jamb_depth,
        braces_enable=fw.braces_enable,
        brace_section_width=fw.brace_section_width,
        brace_section_depth=fw.brace_section_depth,
        brace_min_cell_width=fw.brace_min_cell_width,
        brace_min_cell_height=fw.brace_min_cell_height,
        target_gefach_width=fw.target_gefach_width,
        target_gefach_jitter=fw.target_gefach_jitter,
        z_merge_tol=fw.z_merge_tol,
        roof_pitch_deg=pitch,
        post_section=(post_w, post_d),
    )

    return out, _trace(
        f"WealthPolicy:{w:.3f}",
        [
            ("fachwerk.binder_max", out.binder_max),
            ("fachwerk.roof_pitch_deg", out.roof_pitch_deg),
            ("fachwerk.post_section", out.post_section),
        ],
    )


def _type_layer_hallenhaus(fw: FachwerkPolicySpec, wealth: float) -> tuple[FachwerkPolicySpec, dict[str, ConstraintSpec], TraceLayer]:
    """
    Type-specific anchors:
    - typical binder_max range for hallenhaus
    - constraint specs for sampling/scoring (brustriegel_z, gefach_width_target)
    """
    w = _clamp01(wealth)

    # binder_max typical band for hallenhaus (clamped)
    base = 1.50
    span = 0.15
    binder = base + span * (w - 0.5)
    binder = max(1.40, min(1.65, binder))

    # gefach target: vary mildly with wealth
    target = 1.35 + 0.10 * (w - 0.5)
    target = max(1.20, min(1.50, target))
    jitter = 0.10

    # keep fw defaults except binder_max and target_gefach_*
    fw_out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fw.default_jamb_thickness,
        post_section_width=fw.post_section_width,
        post_section_depth=fw.post_section_depth,
        plate_section_width=fw.plate_section_width,
        plate_section_depth=fw.plate_section_depth,
        opening_jamb_width=fw.opening_jamb_width,
        opening_jamb_depth=fw.opening_jamb_depth,
        braces_enable=fw.braces_enable,
        brace_section_width=fw.brace_section_width,
        brace_section_depth=fw.brace_section_depth,
        brace_min_cell_width=fw.brace_min_cell_width,
        brace_min_cell_height=fw.brace_min_cell_height,
        target_gefach_width=target,
        target_gefach_jitter=jitter,
        z_merge_tol=fw.z_merge_tol,
        roof_pitch_deg=fw.roof_pitch_deg,
        post_section=fw.post_section,
    )

    constraints: dict[str, ConstraintSpec] = {
        "brustriegel_z": ConstraintSpec(
            hard=None,
            soft=RangeSoftSpec(
                ideal=(0.95, 1.10),
                allowed=(0.85, 1.25),
                weight=1.0,
            ),
            unit="m",
            code_prefix="POL",
        ),
        "gefach_width_target": ConstraintSpec(
            hard=RangeHardSpec(0.0, binder),
            soft=RangeSoftSpec(
                ideal=(target - jitter, target + jitter),
                allowed=(1.10, binder),
                weight=3.0,
            ),
            unit="m",
            code_prefix="POL",
        ),
    }

    return fw_out, constraints, _trace(
        "TypePolicy:fachwerkhaus.hallenhaus",
        [
            ("fachwerk.binder_max", fw_out.binder_max),
            ("fachwerk.target_gefach_width", fw_out.target_gefach_width),
            ("fachwerk.target_gefach_jitter", fw_out.target_gefach_jitter),
            ("constraints.brustriegel_z.soft", constraints["brustriegel_z"].soft),
            ("constraints.gefach_width_target.hard", constraints["gefach_width_target"].hard),
            ("constraints.gefach_width_target.soft", constraints["gefach_width_target"].soft),
        ],
    )


# ============================================================
# Public API
# ============================================================


def resolve_policy_stack(ctx: Context) -> ResolvedPolicy:
    resolved, _ = resolve_policy_stack_with_trace(ctx)
    return resolved


def resolve_policy_stack_with_trace(ctx: Context) -> tuple[ResolvedPolicy, ResolutionTrace]:
    house_type = _require_house_type(ctx)
    epoch = _normalize_epoch(ctx.epoch_band)
    settlement = _require_settlement(ctx)

    fw, constraints, l0 = _baseline_layer()
    layers = [l0]

    fw, l1 = _epoch_layer(epoch, fw)
    layers.append(l1)

    fw, l2 = _settlement_layer(settlement, fw)
    layers.append(l2)

    fw, l3 = _wealth_layer(ctx.wealth, fw)
    layers.append(l3)

    if house_type == "fachwerkhaus.hallenhaus":
        fw, type_constraints, l4 = _type_layer_hallenhaus(fw, ctx.wealth)
        layers.append(l4)
        constraints.update(type_constraints)
    else:
        raise PolicyResolutionError(f"Unsupported house_type: {house_type}")

    # Validation (required constraint keys present and only allowed keys used)
    _assert_allowed(
        f"{house_type}.constraints",
        constraints.keys(),
        _ALLOWED_CONSTRAINT_KEYS[house_type],
    )
    missing = _REQUIRED_CONSTRAINT_KEYS[house_type] - set(constraints.keys())
    if missing:
        raise PolicyResolutionError(f"{house_type}: missing required constraints {sorted(missing)}")

    resolved = ResolvedPolicy(
        schema=_POLICY_SCHEMA_VERSION,
        constraints=constraints,
        fachwerk=fw,
    )

    return resolved, ResolutionTrace(
        schema=resolved.schema,
        layers=tuple(layers),
    )
