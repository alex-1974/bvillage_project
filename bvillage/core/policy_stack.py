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

_POLICY_SCHEMA_VERSION = 3

_EPOCH_ALIASES = {
    "E1": "early_medieval",
    "E2": "high_medieval",
    "E3": "late_medieval",
}

_ALLOWED_EPOCHS = {
    "early_medieval",
    "high_medieval",
    "late_medieval",
}

_ALLOWED_SETTLEMENTS = {"rural", "village", "town"}

_ALLOWED_HOUSE_TYPES = {
    "fachwerkhaus.hallenhaus",
}

_ALLOWED_CONSTRAINT_KEYS = {
    "fachwerkhaus.hallenhaus": {
        "brustriegel_z",
        "gefach_width_target",
    }
}

_REQUIRED_CONSTRAINT_KEYS = _ALLOWED_CONSTRAINT_KEYS

_ALLOWED_OVERRIDE_TOPLEVEL = {"fachwerk", "constraints"}
_ALLOWED_FACHWERK_FIELDS = {"binder_max", "default_jamb_thickness"}


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


def _trace(layer_id: str, ops: Iterable[Tuple[str, Any]]) -> TraceLayer:
    return TraceLayer(
        layer_id=layer_id,
        ops=tuple(TraceOp(k, v) for k, v in sorted(ops, key=lambda x: x[0])),
    )


def _assert_allowed(name: str, keys, allowed):
    unknown = set(keys) - set(allowed)
    if unknown:
        raise PolicyResolutionError(f"{name}: unknown keys {sorted(unknown)}")


# ============================================================
# Layer Builders
# ============================================================

def _baseline_layer():
    fachwerk = FachwerkPolicySpec(
        binder_max=1.60,
        default_jamb_thickness=0.20,
    )
    return fachwerk, {}, _trace(
        "BaselinePolicy",
        [
            ("fachwerk.binder_max", fachwerk.binder_max),
            ("fachwerk.default_jamb_thickness", fachwerk.default_jamb_thickness),
        ],
    )


def _epoch_layer(epoch: str, fachwerk: FachwerkPolicySpec):
    binder = fachwerk.binder_max

    if epoch == "early_medieval":
        binder -= 0.05
    elif epoch == "high_medieval":
        pass
    elif epoch == "late_medieval":
        binder += 0.03

    out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fachwerk.default_jamb_thickness,
    )

    return out, _trace(
        f"EpochPolicy:{epoch}",
        [("fachwerk.binder_max", out.binder_max)],
    )


def _settlement_layer(settlement: str, fachwerk: FachwerkPolicySpec):
    if settlement not in _ALLOWED_SETTLEMENTS:
        raise PolicyResolutionError(f"Unsupported settlement_type: {settlement}")

    binder = fachwerk.binder_max

    if settlement == "town":
        binder += 0.02

    out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fachwerk.default_jamb_thickness,
    )

    return out, _trace(
        f"SettlementPolicy:{settlement}",
        [("fachwerk.binder_max", out.binder_max)],
    )


def _wealth_layer(wealth: float, fachwerk: FachwerkPolicySpec):
    w = max(0.0, min(1.0, float(wealth)))
    binder = fachwerk.binder_max + 0.10 * (w - 0.5)

    out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fachwerk.default_jamb_thickness,
    )

    return out, _trace(
        f"WealthPolicy:{w:.3f}",
        [("fachwerk.binder_max", out.binder_max)],
    )


def _type_layer_hallenhaus(fachwerk: FachwerkPolicySpec, wealth: float):
    w = max(0.0, min(1.0, float(wealth)))

    base = 1.50
    span = 0.15
    binder = base + span * (w - 0.5)
    binder = max(1.40, min(1.65, binder))

    fachwerk_out = FachwerkPolicySpec(
        binder_max=binder,
        default_jamb_thickness=fachwerk.default_jamb_thickness,
    )

    target = 1.35 + 0.10 * (w - 0.5)
    target = max(1.20, min(1.50, target))

    constraints = {
        "brustriegel_z": ConstraintSpec(
            hard=None,
            soft=RangeSoftSpec(
                ideal=(0.95, 1.10),
                allowed=(0.85, 1.25),
                weight=1.0,
            ),
        ),
        "gefach_width_target": ConstraintSpec(
            hard=RangeHardSpec(0.0, binder),
            soft=RangeSoftSpec(
                ideal=(target - 0.10, target + 0.10),
                allowed=(1.10, binder),
                weight=3.0,
            ),
        ),
    }

    return fachwerk_out, constraints, _trace(
        "TypePolicy:fachwerkhaus.hallenhaus",
        [
            ("fachwerk.binder_max", fachwerk_out.binder_max),
            ("constraints.brustriegel_z.soft", constraints["brustriegel_z"].soft),
            ("constraints.gefach_width_target.hard", constraints["gefach_width_target"].hard),
        ],
    )


# ============================================================
# Public API
# ============================================================

def resolve_policy_stack(ctx: Context) -> ResolvedPolicy:
    resolved, _ = resolve_policy_stack_with_trace(ctx)
    return resolved


def resolve_policy_stack_with_trace(ctx: Context):
    house_type = _require_house_type(ctx)

    epoch = _normalize_epoch(ctx.epoch_band)
    settlement = ctx.settlement_type

    fachwerk, constraints, l0 = _baseline_layer()
    layers = [l0]

    fachwerk, l1 = _epoch_layer(epoch, fachwerk)
    layers.append(l1)

    fachwerk, l2 = _settlement_layer(settlement, fachwerk)
    layers.append(l2)

    fachwerk, l3 = _wealth_layer(ctx.wealth, fachwerk)
    layers.append(l3)

    if house_type == "fachwerkhaus.hallenhaus":
        fachwerk, type_constraints, l4 = _type_layer_hallenhaus(fachwerk, ctx.wealth)
        layers.append(l4)
        constraints.update(type_constraints)
    else:
        raise PolicyResolutionError(f"Unsupported house_type: {house_type}")

    # Validation
    _assert_allowed(
        f"{house_type}.constraints",
        constraints.keys(),
        _ALLOWED_CONSTRAINT_KEYS[house_type],
    )

    resolved = ResolvedPolicy(
        schema=_POLICY_SCHEMA_VERSION,
        constraints=constraints,
        fachwerk=fachwerk,
    )

    return resolved, ResolutionTrace(
        schema=resolved.schema,
        layers=tuple(layers),
    )
