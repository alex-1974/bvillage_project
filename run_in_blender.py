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

# 2) Import bpy early so we can guard against double-run
try:
    import bpy
except Exception as exc:
    print("IMPORT bpy: FAIL:", repr(exc))
    traceback.print_exc()
    raise

# 3) Singleton guard: prevent double execution in same Blender session
if bpy.app.driver_namespace.get("BVILLAGE_ALREADY_RAN"):
    print("BVILLAGE: already ran once in this Blender session -> skipping.")
    raise SystemExit(0)
bpy.app.driver_namespace["BVILLAGE_ALREADY_RAN"] = True

# 4) Try importing bvillage early with explicit diagnostics
try:
    import bvillage  # noqa: F401
    print("IMPORT bvillage: OK")
except Exception as exc:
    print("IMPORT bvillage: FAIL:", repr(exc))
    print("Contents of PROJECT_ROOT:", os.listdir(PROJECT_ROOT)[:50])
    traceback.print_exc()
    raise

# Optional: hot-reload hygiene after sys.path is correct
for name in list(sys.modules.keys()):
    if name == "bvillage" or name.startswith("bvillage."):
        del sys.modules[name]

# ============================================================
# Run pipeline (guarded)
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

    configure_logging(level="INFO", force=True)

    discover_types(force=True)
    provider = get_house_type(TYPE_ID)

    ctx = Context(
        seed=42,
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
