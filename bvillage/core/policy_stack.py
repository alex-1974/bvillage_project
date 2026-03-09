# bvillage/core/policy_stack.py
from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Iterable

from bvillage.core.model import Context
from bvillage.core.policy_types import (
    ConstraintSpec,
    FachwerkPolicySpec,
    RangeHardSpec,
    RangeSoftSpec,
    ResolvedPolicy,
)

__all__ = [
    "resolve_policy_stack",
    "resolve_policy_stack_with_trace",
    "TraceOp",
    "TraceLayer",
    "ResolutionTrace",
]


# ============================================================
# Trace (artifact contract)
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


def _trace_layer(layer_id: str, ops: Iterable[tuple[str, Any]]) -> TraceLayer:
    return TraceLayer(
        layer_id=str(layer_id),
        ops=tuple(sorted((TraceOp(k, v) for (k, v) in ops), key=lambda o: o.key)),
    )


# ============================================================
# Guards / normalization
# ============================================================

# ------------------------------------------------------------------
# Archetype id compatibility aliases
#
# WHY:
# During migration, old inputs may still use legacy identifiers.
# These aliases normalize legacy values to stable archetype_ids.
# ------------------------------------------------------------------
_ARCHETYPE_ALIASES: dict[str, str] = {
    # canonical examples
    "FW-LH-ND": "FW-LH-ND",
    "FW-LH-2S": "FW-LH-2S",
    "FW-LH-3S": "FW-LH-3S",
    "FW-LH-4S": "FW-LH-4S",
    "FW-GULF": "FW-GULF",
    "FW-HAUB": "FW-HAUB",
    "FW-MITT": "FW-MITT",
    "FW-LH-EN": "FW-LH-EN",
    "FW-STG-GIE": "FW-STG-GIE",
    # legacy / transition aliases
    "hallenhaus": "FW-LH-ND",
    "fachwerk.hallenhaus": "FW-LH-ND",
    "timber_frame.longhouse": "FW-LH-ND",
}

# Context.epoch_band currently uses readable internal names;
# tolerate historic short aliases during migration.
_EPOCH_ALIASES: dict[str, str] = {
    "E1": "early_medieval",
    "E2": "high_medieval",
    "E3": "late_medieval",
    "early_medieval": "early_medieval",
    "high_medieval": "high_medieval",
    "late_medieval": "late_medieval",
}


def _norm_archetype_id(archetype_id: Any) -> str:
    if not isinstance(archetype_id, str) or not archetype_id.strip():
        return "UNKNOWN"
    raw = archetype_id.strip()
    return _ARCHETYPE_ALIASES.get(raw, raw)


def _norm_epoch(epoch_band: Any) -> str:
    if not isinstance(epoch_band, str) or not epoch_band.strip():
        return "unknown"
    raw = epoch_band.strip()
    return _EPOCH_ALIASES.get(raw, raw)


def _clamp01(x: float) -> float:
    v = float(x)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


# ============================================================
# Archetype-family helpers
# ============================================================


def _is_longhouse_family(archetype_id: str) -> bool:
    """
    Return True for archetypes resolved by the timber_frame/longhouse family.

    WHY:
    Policy resolution must no longer depend on plugin path strings such as
    'timber_frame.longhouse'. It should operate on stable archetype ids.
    """
    if archetype_id.startswith("FW-LH-"):
        return True
    if archetype_id in {"FW-GULF", "FW-HAUB", "FW-MITT"}:
        return True
    return False


# ============================================================
# Layers
# ============================================================


def _baseline_fachwerk() -> tuple[FachwerkPolicySpec, TraceLayer]:
    fw = FachwerkPolicySpec(
        binder_max=1.60,
        bay_width=3.645,
        building_width=7.2,
        plate_height=2.6,
        bay_count=5,
        gable_mode="end_frame",
    )
    return fw, _trace_layer(
        "BaselinePolicy",
        [
            ("fachwerk.bay_count", fw.bay_count),
            ("fachwerk.bay_width", fw.bay_width),
            ("fachwerk.binder_max", fw.binder_max),
            ("fachwerk.building_width", fw.building_width),
            ("fachwerk.default_jamb_thickness", fw.default_jamb_thickness),
            ("fachwerk.gable_mode", fw.gable_mode),
            ("fachwerk.plate_height", fw.plate_height),
        ],
    )


def _epoch_layer(epoch: str, fw: FachwerkPolicySpec) -> tuple[FachwerkPolicySpec, TraceLayer]:
    # MVP: epoch currently traced but does not yet modify FachwerkPolicySpec.
    return fw, _trace_layer(
        f"EpochPolicy:{epoch}",
        [
            ("ctx.epoch", epoch),
        ],
    )


def _settlement_layer(settlement: str, fw: FachwerkPolicySpec) -> tuple[FachwerkPolicySpec, TraceLayer]:
    # MVP: settlement currently traced but does not yet modify FachwerkPolicySpec.
    return fw, _trace_layer(
        f"SettlementPolicy:{settlement}",
        [
            ("ctx.settlement_type", settlement),
        ],
    )


def _wealth_layer(wealth01: float, fw: FachwerkPolicySpec) -> tuple[FachwerkPolicySpec, TraceLayer]:
    # Minimal modulation of bay_count to allow larger houses for higher-wealth cases.
    bay_count = fw.bay_count
    if wealth01 >= 0.80:
        bay_count = 7
    elif wealth01 >= 0.60:
        bay_count = 6
    elif wealth01 <= 0.20:
        bay_count = 4

    fw_out = replace(fw, bay_count=int(bay_count))
    return fw_out, _trace_layer(
        f"WealthPolicy:{wealth01:.3f}",
        [
            ("ctx.wealth", wealth01),
            ("fachwerk.bay_count", fw_out.bay_count),
        ],
    )


def _archetype_layer(
    archetype_id: str,
    *,
    epoch: str,
    settlement: str,
    wealth01: float,
    fw: FachwerkPolicySpec,
) -> tuple[FachwerkPolicySpec, dict[str, ConstraintSpec], TraceLayer]:
    """
    Archetype-specific policy resolution.

    Architecture
    ------------
    Resolution is driven by stable archetype_id, not by provider path or folder name.
    """

    constraints: dict[str, ConstraintSpec] = {}

    if _is_longhouse_family(archetype_id):
        # ---- Statics limit (hard structural max spacing) ----
        # Wealth slightly increases span (better timber quality).
        base = 1.50
        span = 0.15
        binder_max = base + span * (wealth01 - 0.5)
        binder_max = max(1.40, min(1.65, binder_max))

        # ---- Cultural target gefach width (aesthetic rhythm) ----
        target_gefach_width = 1.35 + 0.10 * (wealth01 - 0.5)
        target_gefach_width = max(1.20, min(1.50, target_gefach_width))

        jitter = 0.10

        fw_out = replace(
            fw,
            binder_max=float(binder_max),
            target_gefach_width=float(target_gefach_width),
            target_gefach_jitter=float(jitter),
            gable_mode="end_frame",
        )

        constraints["brustriegel_z"] = ConstraintSpec(
            hard=None,
            soft=RangeSoftSpec(
                ideal=(0.95, 1.10),
                allowed=(0.85, 1.25),
                weight=1.0,
            ),
            unit="m",
            code_prefix="LH",
        )

        constraints["gefach_width_target"] = ConstraintSpec(
            hard=RangeHardSpec(0.0, float(binder_max)),
            soft=RangeSoftSpec(
                ideal=(float(target_gefach_width) - float(jitter), float(target_gefach_width) + float(jitter)),
                allowed=(1.10, float(binder_max)),
                weight=3.0,
            ),
            unit="m",
            code_prefix="LH",
        )

        layer = _trace_layer(
            f"ArchetypePolicy:{archetype_id}",
            [
                ("ctx.archetype_id", archetype_id),
                ("ctx.epoch", epoch),
                ("ctx.settlement_type", settlement),
                ("ctx.wealth", wealth01),
                ("fachwerk.bay_count", fw_out.bay_count),
                ("fachwerk.bay_width", fw_out.bay_width),
                ("fachwerk.binder_max", fw_out.binder_max),
                ("fachwerk.building_width", fw_out.building_width),
                ("fachwerk.gable_mode", fw_out.gable_mode),
                ("fachwerk.plate_height", fw_out.plate_height),
                ("constraints.brustriegel_z", "ConstraintSpec"),
                ("constraints.gefach_width_target", "ConstraintSpec"),
                ("gefach.target_width", float(target_gefach_width)),
                ("gefach.jitter", float(jitter)),
            ],
        )

        return fw_out, constraints, layer

    # Generic fallback for unknown / not yet specialized archetypes.
    fw_out = replace(fw, binder_max=1.65)

    layer = _trace_layer(
        f"ArchetypePolicy:{archetype_id}",
        [
            ("ctx.archetype_id", archetype_id),
            ("ctx.epoch", epoch),
            ("ctx.settlement_type", settlement),
            ("ctx.wealth", wealth01),
            ("fachwerk.bay_count", fw_out.bay_count),
            ("fachwerk.bay_width", fw_out.bay_width),
            ("fachwerk.binder_max", fw_out.binder_max),
            ("fachwerk.building_width", fw_out.building_width),
            ("fachwerk.gable_mode", fw_out.gable_mode),
            ("fachwerk.plate_height", fw_out.plate_height),
        ],
    )
    return fw_out, constraints, layer


# ============================================================
# Public API
# ============================================================


def resolve_policy_stack(ctx: Context) -> ResolvedPolicy:
    resolved, _trace = resolve_policy_stack_with_trace(ctx)
    return resolved


def resolve_policy_stack_with_trace(ctx: Context) -> tuple[ResolvedPolicy, ResolutionTrace]:
    """
    Policy resolution driven by canonical archetype_id.

    Notes
    -----
    During migration, legacy ids may still be normalized via _ARCHETYPE_ALIASES.
    """
    archetype_id = _norm_archetype_id(ctx.archetype_id)
    epoch = _norm_epoch(ctx.epoch_band)
    settlement = str(ctx.settlement_type)
    wealth01 = _clamp01(float(ctx.wealth))

    layers: list[TraceLayer] = []

    fw, l0 = _baseline_fachwerk()
    layers.append(l0)

    fw, l1 = _epoch_layer(epoch, fw)
    layers.append(l1)

    fw, l2 = _settlement_layer(settlement, fw)
    layers.append(l2)

    fw, l3 = _wealth_layer(wealth01, fw)
    layers.append(l3)

    fw, constraints, l4 = _archetype_layer(
        archetype_id,
        epoch=epoch,
        settlement=settlement,
        wealth01=wealth01,
        fw=fw,
    )
    layers.append(l4)

    resolved = ResolvedPolicy(
        schema=2,
        constraints=constraints,
        fachwerk=fw,
    )

    trace = ResolutionTrace(
        schema=resolved.schema,
        layers=tuple(layers),
    )

    return resolved, trace
