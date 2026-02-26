# run_in_blender.py
#
# BVILLAGE runner (clean + repeatable)
# - robust project-root discovery
# - optional force re-run inside same Blender session
# - optional hot-reload of bvillage.* modules
# - CLI + env overrides
#
# Usage examples:
#   blender --background --python run_in_blender.py
#   blender --background --python run_in_blender.py -- --seed 123 --type fachwerkhaus.hallenhaus
#   BV_FORCE_RUN=1 blender --background --python run_in_blender.py
#   BV_RELOAD=1 blender --background --python run_in_blender.py -- --force
#
# NOTE: Blender passes args after "--" to the script.

from __future__ import annotations

import argparse
import os
import platform
import sys
import traceback
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Debug banner
# ---------------------------------------------------------------------------

def _banner() -> None:
    print("\n=== BVILLAGE RUNNER START ===")
    print("SCRIPT __file__:", __file__ if "__file__" in globals() else "<no __file__>")
    print("CWD:", os.getcwd())
    print("PYTHON:", sys.version)
    print("EXE:", sys.executable)
    print("PLATFORM:", platform.platform())
    print("sys.path[0:5]:", sys.path[:5])


# ---------------------------------------------------------------------------
# Project root discovery
# ---------------------------------------------------------------------------

def _looks_like_project_root(p: Path) -> bool:
    # Heuristics: must contain package dir "bvillage"
    bv = p / "bvillage"
    if not bv.is_dir():
        return False
    # Often has __init__.py, but allow namespace packages too
    # Additional soft signals:
    return True


def _find_project_root(start: Path, max_up: int = 8) -> Optional[Path]:
    cur = start.resolve()
    for _ in range(max_up + 1):
        if _looks_like_project_root(cur):
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    return None


def _ensure_project_on_syspath() -> Path:
    # Prefer CWD (you run from bvillage_project), else script dir.
    cwd = Path(os.getcwd())
    script_dir = Path(__file__).resolve().parent if "__file__" in globals() else cwd

    root = _find_project_root(cwd) or _find_project_root(script_dir)
    if root is None:
        # Fall back to CWD (better than "/")
        root = cwd.resolve()

    root_s = str(root)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)

    print("PROJECT_ROOT:", root_s)
    print("sys.path[0:5] after:", sys.path[:5])
    return root


# ---------------------------------------------------------------------------
# Blender guard + reload
# ---------------------------------------------------------------------------

def _import_bpy():
    try:
        import bpy  # type: ignore
        return bpy
    except Exception as exc:
        print("IMPORT bpy: FAIL:", repr(exc))
        traceback.print_exc()
        raise


def _should_force_run(args_force: bool) -> bool:
    # Allow env var overrides
    if os.getenv("BV_FORCE_RUN", "0").strip() in ("1", "true", "TRUE", "yes", "YES"):
        return True
    return bool(args_force)


def _should_reload_modules(args_reload: bool) -> bool:
    if os.getenv("BV_RELOAD", "0").strip() in ("1", "true", "TRUE", "yes", "YES"):
        return True
    return bool(args_reload)


def _session_guard(bpy, *, force: bool) -> bool:
    """
    Returns True if we should continue running, False if we should skip.
    Uses bpy.app.driver_namespace as a process-global store.
    """
    ns = bpy.app.driver_namespace
    key = "BVILLAGE_ALREADY_RAN"
    if ns.get(key) and not force:
        print("BVILLAGE: already ran once in this Blender session -> skipping.")
        print("Tip: pass --force or set BV_FORCE_RUN=1")
        return False
    ns[key] = True
    return True


def _reload_bvillage_modules() -> None:
    # Remove bvillage modules so next imports re-read sources.
    # Safe for dev runs; avoid in production runs.
    removed = 0
    for name in list(sys.modules.keys()):
        if name == "bvillage" or name.startswith("bvillage."):
            del sys.modules[name]
            removed += 1
    print(f"Reload: cleared {removed} bvillage modules from sys.modules")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str]) -> argparse.Namespace:
    # Blender passes script args as: blender ... --python run_in_blender.py -- <args>
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--type", default="fachwerkhaus.hallenhaus", help="House type id")
    ap.add_argument("--seed", type=int, default=999, help="Deterministic seed")
    ap.add_argument("--clear", action="store_true", default=True, help="Clear previous build (default true)")
    ap.add_argument("--no-clear", dest="clear", action="store_false", help="Do NOT clear previous build")
    ap.add_argument("--loglevel", default="INFO", help="Logging level (INFO, DEBUG, ...)")
    ap.add_argument("--force", action="store_true", help="Force re-run in same Blender session")
    ap.add_argument("--reload", action="store_true", help="Hot-reload bvillage.* modules before run")
    # Context knobs (keep minimal; expand later)
    ap.add_argument("--epoch", default="late_medieval", help="Context.epoch_band")
    ap.add_argument("--region", default="north", help="Context.region")
    ap.add_argument("--settlement", default="village", help="Context.settlement_type")
    ap.add_argument("--wealth", type=float, default=0.6, help="Context.wealth (0..1)")
    return ap.parse_args(argv)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main() -> int:
    _banner()
    _ensure_project_on_syspath()

    bpy = _import_bpy()
    args = _parse_args(sys.argv)

    force = _should_force_run(args.force)
    if not _session_guard(bpy, force=force):
        return 0

    if _should_reload_modules(args.reload):
        _reload_bvillage_modules()

    # Import bvillage with explicit diagnostics
    try:
        import bvillage  # noqa: F401
        print("IMPORT bvillage: OK")
    except Exception as exc:
        print("IMPORT bvillage: FAIL:", repr(exc))
        traceback.print_exc()
        return 2

    try:
        from bvillage.core.logging_conf import configure_logging
        from bvillage.core.registry import discover_types, get_house_type
        from bvillage.core.report import report_plans
        from bvillage.core.validate import validate
        from bvillage.core.model import Context
        from bvillage.blender.build import build_house

        configure_logging(level=str(args.loglevel).upper(), force=True)

        discover_types(force=True)
        provider = get_house_type(str(args.type))

        ctx = Context(
            seed=int(args.seed),
            epoch_band=str(args.epoch),
            region=str(args.region),
            settlement_type=str(args.settlement),
            wealth=float(args.wealth),
            house_type=str(args.type),
        )

        structure, interior, openings = provider.generate(ctx)
        issues = validate(ctx, structure, interior)
        rep = report_plans(ctx, structure, interior=interior, openings=openings, issues=issues, score=None)
        print(rep)

        build_house(ctx, structure, interior, openings, clear_previous=bool(args.clear))

        print("=== BVILLAGE RUNNER DONE ===\n")
        return 0

    except SystemExit as exc:
        # Avoid Blender spew; treat as clean exit
        code = int(getattr(exc, "code", 0) or 0)
        print(f"=== BVILLAGE RUNNER EXIT ({code}) ===\n")
        return code
    except Exception as exc:
        print("\n=== BVILLAGE RUNNER CRASH ===")
        print("ERROR:", repr(exc))
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    # In Blender, returning is fine; sys.exit is also fine. We avoid hard exits to reduce noise.
    rc = main()
    # If you really want to signal failure in background mode, uncomment:
    # import sys; sys.exit(rc)
