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

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("PROJECT_ROOT:", PROJECT_ROOT)
print("sys.path[0:5] after:", sys.path[:5])

try:
    import bpy
except Exception as exc:
    print("IMPORT bpy: FAIL:", repr(exc))
    traceback.print_exc()
    raise

ns = bpy.app.driver_namespace
ns["BVILLAGE_RUNS"] = int(ns.get("BVILLAGE_RUNS", 0)) + 1
print(f"BVILLAGE: run #{ns['BVILLAGE_RUNS']} (re-run enabled)")

try:
    import bvillage  # noqa: F401
    print("IMPORT bvillage: OK")
except Exception as exc:
    print("IMPORT bvillage: FAIL:", repr(exc))
    print("Contents of PROJECT_ROOT:", os.listdir(PROJECT_ROOT)[:50])
    traceback.print_exc()
    raise

for name in list(sys.modules.keys()):
    if name == "bvillage" or name.startswith("bvillage."):
        del sys.modules[name]

CLEAR_PREVIOUS = True
ARCHETYPE_ID = "FW-LH-ND"

try:
    from bvillage.blender.build import render_house
    from bvillage.core.logging_conf import configure_logging
    from bvillage.core.model import Context
    from bvillage.core.report import report_plans
    from bvillage.core.seed import Seed
    from bvillage.core.site_manager import SiteManager
    from bvillage.core.validate import validate

    configure_logging(level="INFO", force=True)

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
