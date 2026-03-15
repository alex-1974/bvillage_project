#!/usr/bin/env python3
# tools/bvillage_doctor.py

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bvillage.core.dispatch_registry import (
    list_registered_archetypes,
    list_registered_foremen,
    resolve_foreman_for_grammar,
    resolve_provider_for_archetype,
)
from bvillage.core.plugin_bootstrap import ensure_plugins_loaded
from bvillage.core.provider_contract import TypeProvider


OUT_DEFAULT = Path("generated") / "BVILLAGE_DOCTOR.md"


@dataclass(frozen=True, slots=True)
class CheckResult:
    ok: bool
    title: str
    details: tuple[str, ...]


def _has_method(obj: Any, name: str) -> bool:
    return callable(getattr(obj, name, None))


def check_plugin_bootstrap() -> CheckResult:
    try:
        ensure_plugins_loaded()
        return CheckResult(True, "Plugin bootstrap", ("ensure_plugins_loaded() OK",))
    except Exception as exc:
        return CheckResult(False, "Plugin bootstrap", (f"ERROR: {exc!r}",))


def check_archetype_registry() -> tuple[CheckResult, tuple[str, ...]]:
    try:
        archetypes = list_registered_archetypes()
        if not archetypes:
            return CheckResult(False, "Archetype registry", ("No archetypes registered.",)), ()
        return (
            CheckResult(
                True,
                "Archetype registry",
                tuple([f"registered archetypes: {len(archetypes)}", *[f"- {a}" for a in archetypes]]),
            ),
            archetypes,
        )
    except Exception as exc:
        return CheckResult(False, "Archetype registry", (f"ERROR: {exc!r}",)), ()


def check_provider_bindings(archetypes: tuple[str, ...]) -> tuple[CheckResult, dict[str, str]]:
    details: list[str] = []
    grammar_by_archetype: dict[str, str] = {}
    ok = True

    expected_methods = (
        "resolve_policy",
        "plan_structure_and_interior",
        "plan_openings_for_type",
        "validate_for_type",
    )

    for archetype in archetypes:
        try:
            binding = resolve_provider_for_archetype(archetype)
        except Exception as exc:
            ok = False
            details.append(f"- {archetype}: ERROR resolving binding: {exc!r}")
            continue

        provider = binding.provider
        grammar = binding.construction_grammar
        grammar_by_archetype[archetype] = grammar

        details.append(f"- {archetype}: provider={provider.__class__.__name__}, grammar={grammar}")

        if not isinstance(provider, TypeProvider):
            ok = False
            details.append(f"  - FAIL: provider does not satisfy TypeProvider runtime protocol")

        for method in expected_methods:
            if not _has_method(provider, method):
                ok = False
                details.append(f"  - FAIL: missing method {method}()")

    if not details:
        details.append("No provider bindings checked.")

    return CheckResult(ok, "Provider bindings", tuple(details)), grammar_by_archetype


def check_foremen(grammar_by_archetype: dict[str, str]) -> CheckResult:
    details: list[str] = []
    ok = True

    try:
        registered = list_registered_foremen()
        details.append(f"registered foremen: {len(registered)}")
        for grammar in registered:
            details.append(f"- {grammar}")
    except Exception as exc:
        return CheckResult(False, "Foreman registry", (f"ERROR listing foremen: {exc!r}",))

    needed = sorted(set(grammar_by_archetype.values()))
    for grammar in needed:
        try:
            foreman = resolve_foreman_for_grammar(grammar)
        except Exception as exc:
            ok = False
            details.append(f"- {grammar}: ERROR resolving foreman: {exc!r}")
            continue

        details.append(f"- {grammar}: foreman={foreman.__class__.__name__}")

        if not _has_method(foreman, "dispatch"):
            ok = False
            details.append("  - FAIL: missing dispatch()")

        if not hasattr(foreman, "pipeline_mode"):
            ok = False
            details.append("  - FAIL: missing pipeline_mode")

    return CheckResult(ok, "Foreman registry", tuple(details))


def render_markdown(results: list[CheckResult]) -> str:
    all_ok = all(r.ok for r in results)

    lines: list[str] = []
    lines.append("# BVILLAGE DOCTOR")
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append(f"- status: `{'OK' if all_ok else 'FAIL'}`")
    lines.append("")

    for result in results:
        lines.append(f"## {result.title}")
        lines.append("")
        lines.append(f"- status: `{'OK' if result.ok else 'FAIL'}`")
        lines.append("")
        for detail in result.details:
            lines.append(detail)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Runtime diagnostics for BVILLAGE plugin/bootstrap/dispatch setup.")
    parser.add_argument("--out", default=str(OUT_DEFAULT), help="Markdown output path.")
    args = parser.parse_args()

    results: list[CheckResult] = []

    r_boot = check_plugin_bootstrap()
    results.append(r_boot)

    r_arch, archetypes = check_archetype_registry()
    results.append(r_arch)

    r_bind, grammar_by_archetype = check_provider_bindings(archetypes)
    results.append(r_bind)

    r_foreman = check_foremen(grammar_by_archetype)
    results.append(r_foreman)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_markdown(results), encoding="utf-8")

    print(f"Wrote {out}")
    overall_ok = all(r.ok for r in results)
    print(f"Status: {'OK' if overall_ok else 'FAIL'}")

    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
