#!/usr/bin/env python3
# run_in_blender.py

import os
import platform
import sys
import traceback

print("\n=== BVILLAGE RUNNER START ===")

print("SCRIPT __file__:", __file__ if "__file__" in globals() else "<no __file__>")
print("CWD:", os.getcwd())
print("PYTHON:", sys.version)
print("EXE:", sys.executable)
print("PLATFORM:", platform.platform())
print("sys.path[0:5]:", sys.path[:5])

# ------------------------------------------------------------
# PROJECT ROOT
# ------------------------------------------------------------

PROJECT_ROOT = os.getcwd()

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("PROJECT_ROOT:", PROJECT_ROOT)
print("sys.path[0:5] after:", sys.path[:5])


# ------------------------------------------------------------
# Blender import
# ------------------------------------------------------------

try:
    import bpy
except Exception as exc:
    print("IMPORT bpy: FAIL:", repr(exc))
    traceback.print_exc()
    raise


# ------------------------------------------------------------
# BVILLAGE module reset (DEV convenience)
# ------------------------------------------------------------

DEV_RESET = True

if DEV_RESET:
    for name in list(sys.modules.keys()):
        if name == "bvillage" or name.startswith("bvillage."):
            del sys.modules[name]


# ------------------------------------------------------------
# BVILLAGE imports (fresh after reset)
# ------------------------------------------------------------

try:
    import bvillage
    print("IMPORT bvillage: OK")
except Exception as exc:
    print("IMPORT bvillage: FAIL:", repr(exc))
    traceback.print_exc()
    raise


from bvillage.core.trace import (
    configure_trace,
    trace_enabled_from_env,
    get_trace,
)

from bvillage.core.logging_conf import configure_logging
from bvillage.core.model import Context
from bvillage.core.report import report_plans
from bvillage.core.seed import Seed
from bvillage.core.site_manager import SiteManager
from bvillage.core.validate import validate

from bvillage.blender.build import render_house


# ------------------------------------------------------------
# TRACE configuration
# ------------------------------------------------------------

configure_trace(
    enabled=trace_enabled_from_env(),
    out_path="generated/PIPELINE_TRACE.txt",
)


# ------------------------------------------------------------
# Blender run counter (re-run convenience)
# ------------------------------------------------------------

ns = bpy.app.driver_namespace
ns["BVILLAGE_RUNS"] = int(ns.get("BVILLAGE_RUNS", 0)) + 1

print(f"BVILLAGE: run #{ns['BVILLAGE_RUNS']} (re-run enabled)")


# ------------------------------------------------------------
# MAIN RUN
# ------------------------------------------------------------

try:

    configure_logging(level="INFO", force=True)

    ARCHETYPE_ID = "FW-LH-ND"
    CLEAR_PREVIOUS = True

    ctx = Context(
        seed=Seed(42),
        epoch_band="late_medieval",
        region="north",
        settlement_type="village",
        wealth=0.6,
        archetype_id=ARCHETYPE_ID,
    )

    manager = SiteManager()

    structure, interior, openings = manager.build(ctx)


    # --------------------------------------------------------
    # TRACE OUTPUT
    # --------------------------------------------------------

    trace = get_trace()

    if trace.enabled:

        print()
        print("=== BVILLAGE PIPELINE TRACE ===")
        print()

        print(trace.render_text())

        path = trace.write_report()

        if path:
            print()
            print(f"Trace written to: {path}")


    # --------------------------------------------------------
    # VALIDATION + REPORT
    # --------------------------------------------------------

    issues = validate(ctx, structure, interior)

    rep = report_plans(
        ctx,
        structure,
        interior=interior,
        openings=openings,
        issues=issues,
        score=None,
    )

    print(rep)


    # --------------------------------------------------------
    # BLENDER BUILD
    # --------------------------------------------------------

    render_house(
        ctx,
        structure,
        interior,
        openings,
        clear_previous=CLEAR_PREVIOUS,
    )

    print("=== BVILLAGE RUNNER DONE ===\n")


except Exception as exc:

    print("\n=== BVILLAGE RUNNER CRASH ===")
    print("ERROR:", repr(exc))
    traceback.print_exc()
    raise
