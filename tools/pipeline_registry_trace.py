#!/usr/bin/env python3
# tools/pipeline_registry_trace.py

"""Pipeline trace report for BVILLAGE plugin dispatch and stage ownership.

This tool is intentionally read-only. It does not generate geometry and does
not mutate repository files. Its purpose is to make the effective pipeline for
an archetype visible before or during debugging.

What it reports
---------------
- plugin bootstrap status
- resolved ArchetypeBinding data
- provider / foreman classes actually selected for an archetype
- inferred specialist objects exposed by the provider/foreman
- expected artifact flow across the canonical pipeline
- optional user-supplied order / policy context summary

What it does not do
-------------------
- it does not force a full building generation
- it does not invent missing runtime objects
- it does not assume a concrete entrypoint outside the visible registry APIs

Rationale
---------
BVILLAGE already has static architecture tools (import graph, call graph,
audit). What is still needed in practice is a stage-level view of the concrete
pipeline selected for a given archetype. This script fills that gap with a
conservative, registry-first trace.

Usage
-----
    python3 tools/pipeline_trace.py --archetype FW-LH-ND
    python3 tools/pipeline_trace.py --archetype FW-LH-ND --json
    python3 tools/pipeline_trace.py --archetype FW-LH-ND --context trace_ctx.json
    python3 tools/pipeline_trace.py --archetype FW-LH-ND --out generated/PIPELINE_TRACE.md
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


# ------------------------------------------------------------
# Make project root importable
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from bvillage.core.foreman.plan_bootstrap import ensure_plugins_loaded
from bvillage.core.foreman.plan_dispatch import (
    list_registered_archetypes,
    resolve_provider_for_archetype,
)


# ASSUMED — not verified against current codebase:
# - The stable public registry entrypoints are ensure_plugins_loaded(),
#   list_registered_archetypes(), and resolve_provider_for_archetype().
# - resolve_provider_for_archetype(archetype_id) returns a binding object with
#   at least a provider attribute and usually additional metadata such as
#   archetype_id, type_family, domain, and construction_grammar.
# - Provider / foreman implementations may expose specialist objects either as
#   attributes (e.g. topology_planner, frame_producer) or indirectly via
#   descriptive methods / pipeline metadata.


DEFAULT_OUT_DIR = "generated"
TRACE_BANNER = "BVILLAGE PIPELINE TRACE"


@dataclass(frozen=True, slots=True)
class TraceStage:
    name: str
    owner: str
    resolved_object: str
    contract_input: tuple[str, ...]
    contract_output: tuple[str, ...]
    notes: tuple[str, ...] = ()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Trace BVILLAGE pipeline ownership for one archetype.")
    parser.add_argument("--archetype", required=True, help="Archetype ID to trace, e.g. FW-LH-ND")
    parser.add_argument(
        "--context",
        default="",
        help="Optional JSON file with BuildingOrder- or context-like data to summarize in the trace.",
    )
    parser.add_argument("--json", action="store_true", help="Write JSON instead of Markdown text.")
    parser.add_argument("--out", default="", help="Explicit output path.")
    return parser.parse_args()


def resolve_outfile(root: Path, archetype_id: str, as_json: bool, out: str) -> Path:
    if out:
        p = Path(out)
        if not p.is_absolute():
            p = root / p
        return p
    suffix = "json" if as_json else "md"
    filename = f"PIPELINE_TRACE_{_slug(archetype_id)}.{suffix}"
    return root / DEFAULT_OUT_DIR / filename


def _slug(text: str) -> str:
    safe = []
    for ch in text:
        if ch.isalnum() or ch in {"-", "_"}:
            safe.append(ch)
        else:
            safe.append("_")
    return "".join(safe)


def _class_name(obj: Any) -> str:
    if obj is None:
        return "(none)"
    cls = obj.__class__
    return f"{cls.__module__}.{cls.__name__}"


def _safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(obj, name)
    except Exception:
        return default


def _binding_metadata(binding: Any) -> dict[str, Any]:
    keys = (
        "archetype_id",
        "type_family",
        "domain",
        "construction_grammar",
        "provider",
    )
    out: dict[str, Any] = {}
    for key in keys:
        out[key] = _safe_getattr(binding, key)
    return out


def _context_summary(path_str: str) -> dict[str, Any]:
    if not path_str:
        return {}
    path = Path(path_str)
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("Context JSON must decode to an object at top level.")
    return data


def _infer_specialists(provider: Any) -> dict[str, Any]:
    attr_candidates = {
        "foreman": ("foreman", "site_manager", "dispatcher"),
        "topology_planner": ("topology_planner", "planner", "topology_provider"),
        "frame_producer": ("frame_producer", "structural_producer", "domain_engine"),
        "roof_producer": ("roof_producer", "roof_builder"),
        "joiner": ("joiner", "interior_planner"),
        "inspector": ("inspector", "physics_validator"),
        "appraiser": ("appraiser", "evaluator", "candidate_auditor"),
        "renderer": ("renderer", "builder", "blender_builder"),
    }

    found: dict[str, Any] = {}
    for label, names in attr_candidates.items():
        for name in names:
            value = _safe_getattr(provider, name)
            if value is not None:
                found[label] = value
                break

    foreman = found.get("foreman")
    if foreman is not None:
        for label, names in attr_candidates.items():
            if label in found:
                continue
            for name in names:
                value = _safe_getattr(foreman, name)
                if value is not None:
                    found[label] = value
                    break

    return found


def _infer_pipeline_mode(provider: Any, specialists: dict[str, Any]) -> str:
    for obj in (provider, specialists.get("foreman")):
        if obj is None:
            continue
        value = _safe_getattr(obj, "pipeline_mode")
        if value is not None:
            return str(value)
    return "(not exposed)"


def _canonical_stages(provider: Any, binding_meta: dict[str, Any], specialists: dict[str, Any]) -> tuple[TraceStage, ...]:
    foreman_obj = specialists.get("foreman", provider)
    return (
        TraceStage(
            name="Commissioner / BuildingOrder",
            owner="core",
            resolved_object="(external caller)",
            contract_input=("Context",),
            contract_output=("BuildingOrder", "ResolvedPolicy"),
            notes=("Commissioner is outside this trace tool; optional context JSON is summarized separately.",),
        ),
        TraceStage(
            name="Foreman",
            owner=str(binding_meta.get("domain") or "plugin"),
            resolved_object=_class_name(foreman_obj),
            contract_input=("BuildingOrder",),
            contract_output=("dispatch decisions",),
            notes=(f"pipeline_mode={_infer_pipeline_mode(provider, specialists)}",),
        ),
        TraceStage(
            name="Topology Planner",
            owner=str(binding_meta.get("type_family") or "type plugin"),
            resolved_object=_class_name(specialists.get("topology_planner")),
            contract_input=("BuildingOrder", "ResolvedPolicy"),
            contract_output=("SemanticPlan",),
        ),
        TraceStage(
            name="Frame Producer",
            owner=str(binding_meta.get("construction_grammar") or "domain plugin"),
            resolved_object=_class_name(specialists.get("frame_producer")),
            contract_input=("SemanticPlan", "ResolvedPolicy"),
            contract_output=("FramePlan",),
        ),
        TraceStage(
            name="Roof Producer",
            owner=str(binding_meta.get("construction_grammar") or "domain plugin"),
            resolved_object=_class_name(specialists.get("roof_producer")),
            contract_input=("FramePlan", "ResolvedPolicy"),
            contract_output=("RoofPlan",),
        ),
        TraceStage(
            name="Joiner",
            owner=str(binding_meta.get("type_family") or "type plugin"),
            resolved_object=_class_name(specialists.get("joiner")),
            contract_input=("SemanticPlan", "FramePlan", "ResolvedPolicy"),
            contract_output=("InteriorPlan",),
        ),
        TraceStage(
            name="Inspector",
            owner="core",
            resolved_object=_class_name(specialists.get("inspector")),
            contract_input=("FramePlan", "RoofPlan", "InteriorPlan", "SemanticPlan"),
            contract_output=("ValidationReport",),
        ),
        TraceStage(
            name="Appraiser",
            owner="core",
            resolved_object=_class_name(specialists.get("appraiser")),
            contract_input=("ValidationReport", "ConstraintsPolicy"),
            contract_output=("CandidateScore",),
        ),
        TraceStage(
            name="Renderer",
            owner="blender",
            resolved_object=_class_name(specialists.get("renderer")),
            contract_input=("FramePlan", "RoofPlan", "InteriorPlan"),
            contract_output=("Blender Geometry",),
            notes=("Renderer must emit from explicit artifacts only.",),
        ),
    )


def _specialist_summary(specialists: dict[str, Any]) -> dict[str, str]:
    ordered = (
        "foreman",
        "topology_planner",
        "frame_producer",
        "roof_producer",
        "joiner",
        "inspector",
        "appraiser",
        "renderer",
    )
    return {key: _class_name(specialists.get(key)) for key in ordered}


def _json_ready_context(data: dict[str, Any]) -> dict[str, Any]:
    keep = (
        "archetype_id",
        "world_seed",
        "settlement_seed",
        "house_salt",
        "plot_constraints",
        "resolved_policy",
        "policy",
        "region",
        "epoch_band",
        "settlement_type",
        "wealth",
        "building_use",
    )
    return {key: data[key] for key in keep if key in data}


def build_trace(archetype_id: str, context_data: dict[str, Any]) -> dict[str, Any]:
    ensure_plugins_loaded()

    archetypes = tuple(list_registered_archetypes())
    if archetype_id not in archetypes:
        raise RuntimeError(
            f"Archetype {archetype_id!r} is not registered. Available archetypes: {', '.join(archetypes)}"
        )

    binding = resolve_provider_for_archetype(archetype_id)
    binding_meta = _binding_metadata(binding)
    provider = binding_meta["provider"]
    specialists = _infer_specialists(provider)
    stages = _canonical_stages(provider, binding_meta, specialists)

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "project_root": str(PROJECT_ROOT),
        "trace_kind": "registry-first pipeline trace",
        "archetype_id": archetype_id,
        "registered_archetypes": archetypes,
        "binding": {
            "archetype_id": binding_meta.get("archetype_id"),
            "type_family": binding_meta.get("type_family"),
            "domain": binding_meta.get("domain"),
            "construction_grammar": binding_meta.get("construction_grammar"),
            "provider_class": _class_name(provider),
        },
        "pipeline_mode": _infer_pipeline_mode(provider, specialists),
        "specialists": _specialist_summary(specialists),
        "context_summary": _json_ready_context(context_data),
        "stages": [
            {
                "name": stage.name,
                "owner": stage.owner,
                "resolved_object": stage.resolved_object,
                "contract_input": list(stage.contract_input),
                "contract_output": list(stage.contract_output),
                "notes": list(stage.notes),
            }
            for stage in stages
        ],
    }


def render_markdown(trace: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {TRACE_BANNER}\n")
    lines.append(f"Generated: {trace['generated_at']}")
    lines.append(f"Project root: `{trace['project_root']}`")
    lines.append(f"Trace kind: {trace['trace_kind']}\n")

    lines.append("## Binding\n")
    binding = trace["binding"]
    lines.append(f"- Archetype: `{binding.get('archetype_id') or trace['archetype_id']}`")
    lines.append(f"- Type family: `{binding.get('type_family')}`")
    lines.append(f"- Domain: `{binding.get('domain')}`")
    lines.append(f"- Construction grammar: `{binding.get('construction_grammar')}`")
    lines.append(f"- Provider: `{binding.get('provider_class')}`")
    lines.append(f"- Pipeline mode: `{trace['pipeline_mode']}`\n")

    ctx = trace.get("context_summary") or {}
    if ctx:
        lines.append("## Input context summary\n")
        for key, value in ctx.items():
            value_text = json.dumps(value, ensure_ascii=False, sort_keys=True)
            lines.append(f"- `{key}`: `{value_text}`")
        lines.append("")

    lines.append("## Resolved specialists\n")
    for key, value in trace["specialists"].items():
        lines.append(f"- `{key}` → `{value}`")
    lines.append("")

    lines.append("## Stage trace\n")
    for idx, stage in enumerate(trace["stages"], start=1):
        lines.append(f"### {idx}. {stage['name']}\n")
        lines.append(f"- Owner: `{stage['owner']}`")
        lines.append(f"- Resolved object: `{stage['resolved_object']}`")
        lines.append(f"- Input: `{', '.join(stage['contract_input'])}`")
        lines.append(f"- Output: `{', '.join(stage['contract_output'])}`")
        if stage["notes"]:
            for note in stage["notes"]:
                lines.append(f"- Note: {note}")
        lines.append("")

    lines.append("## Interpretation\n")
    lines.append("This report is conservative. It traces the selected plugin chain and the contractual artifact flow.")
    lines.append("It does not claim that every unresolved specialist is absent from the system; it only states that the object is not exposed through the visible registry/provider surface used here.")
    lines.append("")
    lines.append("## Invariants checked implicitly\n")
    lines.append("- Plugins bootstrap successfully.")
    lines.append("- The archetype is registered.")
    lines.append("- A provider binding exists for the archetype.")
    lines.append("- The pipeline is reported in members-first artifact order: SemanticPlan → FramePlan → RoofPlan → InteriorPlan → Renderer.")
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    context_data = _context_summary(args.context)
    trace = build_trace(archetype_id=args.archetype, context_data=context_data)

    out = resolve_outfile(PROJECT_ROOT, args.archetype, args.json, args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.json:
        out.write_text(json.dumps(trace, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    else:
        out.write_text(render_markdown(trace), encoding="utf-8")

    print(f"Pipeline trace written to {out}")


if __name__ == "__main__":
    main()
