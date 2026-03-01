# bvillage/core/report.py

"""
bvillage.core.report
===================

Purpose
-------
Human-readable reports for generated plans (structure/interior/openings)
and their validation results.

Design
------
- Pure formatting: no side effects, no logging configuration, no prints.
- Stable output ordering for diffs/debugging.
- Internal base unit is meters; formatting uses bvillage.core.units helpers.

Performance: trivial (small lists).
"""

from __future__ import annotations

from typing import List, Sequence

from bvillage.core.units import fmt_m, fmt_range_m
from .model import Context, StructurePlan, InteriorPlan, OpeningsPlan, Issue, Score


def report_plans(
    ctx: Context,
    structure: StructurePlan,
    interior: InteriorPlan | None = None,
    openings: OpeningsPlan | None = None,
    issues: Sequence[Issue] | None = None,
    score: Score | None = None,
) -> str:
    """
    Build a comprehensive multi-section report.

    Parameters
    ----------
    ctx:
        Generation context.
    structure:
        StructurePlan.
    interior:
        Optional InteriorPlan.
    openings:
        Optional OpeningsPlan.
    issues:
        Optional list of validation issues.
    score:
        Optional Score summary.

    Returns
    -------
    str
        Multi-line report.
    """
    lines: List[str] = []
    fp = structure.footprint

    lines.append("========== BVILLAGE REPORT ==========")
    lines.append(
        "[Context] "
        f"type={ctx.house_type} seed={ctx.seed.base} "
        f"epoch={ctx.epoch_band} region={ctx.region} settlement={ctx.settlement_type} "
        f"wealth={ctx.wealth:.2f}"
    )
    lines.append(
        "[Dims] "
        f"L={fmt_m(fp.length)} W={fmt_m(fp.width)} "
        f"stories={structure.stories} rot={fp.orientation_deg:.1f}°"
    )

    # Grid summary
    gx = structure.grid.axes_u
    gy = structure.grid.axes_v
    lines.append(f"[Grid] axes_u n={len(gx)} axes_v n={len(gy)} fields n={len(structure.grid.fields)}")
    if len(gx) <= 25:
        lines.append("  axes_u: " + ", ".join(f"{v:.3f}" for v in gx))
    if len(gy) <= 25:
        lines.append("  axes_v: " + ", ".join(f"{v:.3f}" for v in gy))

    # Frames
    lines.append(f"[Frames] n={len(structure.frames)}")
    for fr in structure.frames[:30]:
        lines.append(f"  {fr.id}: bay_index={fr.bay_index} tags={list(fr.tags)}")
    if len(structure.frames) > 30:
        lines.append(f"  ... (+{len(structure.frames) - 30} more)")

    # Walls
    lines.append(f"[Walls] n={len(structure.walls)}")
    for w in structure.walls:
        lines.append(
            f"  {w.id} side={w.side} "
            f"u={fmt_range_m(w.u_axis[0], w.u_axis[1])} "
            f"z={fmt_range_m(w.z_range[0], w.z_range[1])} "
            f"tags={list(w.tags)}"
        )

    # Reserved
    lines.append(f"[Reserved] n={len(structure.reserved_slots)}")
    for rs in structure.reserved_slots:
        lines.append(f"  {rs.id}: field={rs.field_id} tags={list(rs.tags)}")

    # Interior
    if interior is not None:
        lines.append(f"[Zones] n={len(interior.zones)}")
        for z in interior.zones:
            lines.append(f"  {z.id} fields={len(z.field_ids)} tags={list(z.tags)}")

        lines.append(f"[Rooms] n={len(interior.rooms)}")
        for r in interior.rooms:
            lines.append(f"  {r.id} type={r.type} story={r.story} fields={len(r.field_ids)}")

        lines.append(f"[Doors] n={len(interior.doors)}")
        for d in interior.doors:
            lines.append(
                f"  {d.id} between={d.between} wall_ref={d.wall_ref} "
                f"w={d.width:.2f} z={fmt_range_m(d.z_range[0], d.z_range[1])} tags={list(d.tags)}"
            )

        lines.append(f"[OpeningDemands] n={len(interior.opening_demands)}")
        for od in interior.opening_demands:
            lines.append(
                f"  room={od.room_id} pref={od.wall_preference} min={od.min_count} max={od.max_count} tags={list(od.tags)}"
            )

    # Openings
    if openings is not None:
        lines.append(f"[Openings] n={len(openings.openings)}")
        for o in openings.openings:
            lines.append(
                f"  {o.id} type={o.type} wall={o.wall_id} "
                f"u={fmt_range_m(o.u_axis[0], o.u_axis[1])} "
                f"z={fmt_range_m(o.z_range[0], o.z_range[1])} "
                f"anim={o.animation}"
            )

    # Issues
    if issues is not None:
        hard = sum(1 for i in issues if i.severity == "HARD")
        soft = sum(1 for i in issues if i.severity == "SOFT")
        sug = sum(1 for i in issues if i.severity == "SUGGEST")
        lines.append(f"[Issues] hard={hard} soft={soft} suggest={sug} total={len(issues)}")

        for i in list(issues)[:50]:
            lines.append(
                f"  - {i.severity} {i.code}: {i.message} "
                f"rel={list(i.related_ids)} repairs={list(i.suggested_repairs)}"
            )
        if len(issues) > 50:
            lines.append(f"  ... (+{len(issues) - 50} more)")

    # Score
    if score is not None:
        lines.append(
            f"[Score] P={score.plausibility:.3f} U={score.usability:.3f} "
            f"V={score.variety:.3f} T={score.total:.3f}"
        )

    return "\n".join(lines)
