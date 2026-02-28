# run_in_blender.py

import os
import sys
import traceback
import platform

# --- HARD DEBUG BANNER (prints always) ---
print("\n=== BVILLAGE RUNNER START ===")
print("SCRIPT __file__:", __file__ if "__file__" in globals() else "<no __file__>")
print("CWD:", os.getcwd())
print("PYTHON:", sys.version)
print("EXE:", sys.executable)
print("PLATFORM:", platform.platform())
print("sys.path[0:5]:", sys.path[:5])

# 1) Make project root importable (root = folder containing THIS file)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("PROJECT_ROOT:", PROJECT_ROOT)
print("sys.path[0:5] after:", sys.path[:5])

# 2) Import bpy early so we can use driver_namespace for in-session state
try:
    import bpy
except Exception as exc:
    print("IMPORT bpy: FAIL:", repr(exc))
    traceback.print_exc()
    raise

# 3) Allow re-run in the same Blender session (Scripting: Run Script)
#    We keep a counter for diagnostics instead of blocking.
ns = bpy.app.driver_namespace
ns["BVILLAGE_RUNS"] = int(ns.get("BVILLAGE_RUNS", 0)) + 1
print(f"BVILLAGE: run #{ns['BVILLAGE_RUNS']} (re-run enabled)")

# 4) Try importing bvillage early with explicit diagnostics
try:
    import bvillage  # noqa: F401
    print("IMPORT bvillage: OK")
except Exception as exc:
    print("IMPORT bvillage: FAIL:", repr(exc))
    print("Contents of PROJECT_ROOT:", os.listdir(PROJECT_ROOT)[:50])
    traceback.print_exc()
    raise

# 5) Hot-reload hygiene: drop bvillage modules so edits are picked up on rerun
for name in list(sys.modules.keys()):
    if name == "bvillage" or name.startswith("bvillage."):
        del sys.modules[name]

# ============================================================
# Run pipeline (re-runnable)
# ============================================================

CLEAR_PREVIOUS = True
TYPE_ID = "fachwerkhaus.hallenhaus"

try:
    from bvillage.core.logging_conf import configure_logging
    from bvillage.core.registry import discover_types, get_house_type
    from bvillage.core.report import report_plans
    from bvillage.core.validate import validate
    from bvillage.core.model import Context
    from bvillage.blender.build import build_house
    from bvillage.core.seed import Seed

    configure_logging(level="INFO", force=True)

    discover_types(force=True)
    provider = get_house_type(TYPE_ID)

    ctx = Context(
        seed=Seed(42),
        epoch_band="late_medieval",
        region="north",
        settlement_type="village",
        wealth=0.6,
        house_type=TYPE_ID,
    )

    structure, interior, openings = provider.generate(ctx)
    issues = validate(ctx, structure, interior)
    rep = report_plans(ctx, structure, interior=interior, openings=openings, issues=issues, score=None)
    print(rep)

    build_house(ctx, structure, interior, openings, clear_previous=CLEAR_PREVIOUS)

    print("=== BVILLAGE RUNNER DONE ===\n")

except Exception as exc:
    print("\n=== BVILLAGE RUNNER CRASH ===")
    print("ERROR:", repr(exc))
    traceback.print_exc()
    raise
