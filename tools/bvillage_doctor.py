#!/usr/bin/env python3
# tools/bvillage_doctor.py

from __future__ import annotations

import os
import sys


# ------------------------------------------------------------
# Make project root importable
# ------------------------------------------------------------

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from bvillage.core.provider_contract import TypeProvider
from bvillage.core.foreman.plan_bootstrap import ensure_plugins_loaded
from bvillage.core.foreman.plan_dispatch import (
    list_registered_archetypes,
    resolve_provider_for_archetype,
)


def check_plugins() -> None:
    print("Loading plugins...")
    ensure_plugins_loaded()
    print("✓ plugins loaded")


def check_archetypes() -> tuple[str, ...]:
    print("Checking archetype registry...")

    archetypes = list_registered_archetypes()

    if not archetypes:
        raise RuntimeError("No archetypes registered")

    print(f"✓ {len(archetypes)} archetypes registered")
    for archetype_id in archetypes:
        print(f"  - {archetype_id}")

    return archetypes


def check_provider_contracts(archetypes: tuple[str, ...]) -> None:
    print("Checking provider contracts...")

    seen: dict[str, list[str]] = {}

    for archetype_id in archetypes:
        binding = resolve_provider_for_archetype(archetype_id)
        provider = binding.provider

        if not isinstance(provider, TypeProvider):
            raise RuntimeError(
                f"Provider for {archetype_id} does not satisfy TypeProvider contract"
            )

        seen.setdefault(provider.__class__.__name__, []).append(archetype_id)

    for provider_name, ids in seen.items():
        print(f"✓ provider {provider_name}: {len(ids)} archetypes")


def main() -> None:
    print()
    print("BVILLAGE SYSTEM DIAGNOSTICS")
    print("===========================")
    print()

    try:
        check_plugins()
        archetypes = check_archetypes()
        check_provider_contracts(archetypes)
    except Exception as exc:
        print()
        print("✗ SYSTEM ERROR")
        print(exc)
        print()
        sys.exit(1)

    print()
    print("✓ system OK")
    print()


if __name__ == "__main__":
    main()
