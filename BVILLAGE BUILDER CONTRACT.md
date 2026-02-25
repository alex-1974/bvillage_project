# BVILLAGE – BUILDER CONTRACT
Status: ACTIVE
Scope: Domain Blender Builders (e.g. bvillage.domains.fachwerk.blender.*)

## 1. Purpose
Builders are geometry emitters. They must not compute or "repair" constructive logic.
All constructive decisions happen in domain-core and are stored as artifacts.

## 2. Artifact Source of Truth
Builders must obtain their constructive input from StructurePlan.notes using the notes schema:

notes["domains"][<domain>][<artifact>]

Canonical accessor:
- bvillage.core.notes.get_domain_artifact()

Legacy aliases may be read (transitional) but must not be written by builders.

## 3. Required Artifact: fachwerk.frameplan
Domain: "fachwerk"
Artifact: "frameplan"

Payload schema: `frameplan_to_dict()` output.

Required keys:
- fp["dims"] = {"L","W","H_e","z0"}
- fp["axes_u"] = dict per wall { "primary","opening","secondary","all" }
- fp["axes_z"] = list[float]
- fp["openings"] = list[ {wall,u0,u1,z0,z1,...} ]
Optional keys:
- fp["z_repair_log"]
- fp["wall_tags"]
- fp["front_wall"]

NOTE:
- axes_u and axes_z are authoritative for structural placement.
- openings are authoritative for exclusion zones (infills) and for opening frames.

## 4. Builder Input Rules
Builders may read:
- StructurePlan.footprint (for coordinate frame)
- StructurePlan.grid (for interior-only helpers, not structure)
- StructurePlan.notes (for artifacts)
- Context metadata (for naming/debug)

Builders must not:
- derive axes from grid
- invent missing axes or "fix" them
- ignore fp axes in favor of axis_x or axis_y
- mutate plans or notes

## 5. Determinism
Builders must:
- use deterministic naming
- iterate walls in fixed order (N,S,E,W)
- iterate u/z axes in sorted order
- never call random directly (no RNG in builders)

## 6. Repairs & Debug
Repairs belong to domain-core. Builder may only display debug helpers.
Debug helpers must never break the build (must be exception-safe).

## 7. Output Structure
Builders should create a domain subtree under the house root:
- <HouseName>_Fachwerk/
  - Frame/
  - Roof/
  - Openings/
  - Infills/
  - Debug/

Clearing:
- Clearing behavior is controlled by runner; builders must not force-clear by default.

# FramePlan Interface (Authoritative)

The BlenderBuilder must build from explicit structural members.

FramePlan MUST contain:

FramePlan = {
  "axes_u": { ... },
  "axes_z": [...],
  "openings": [...],

  "members": {
     "posts": [
        { "wall": "...", "u": ..., "z0": ..., "z1": ..., "role": "stud|corner|..." }
     ],
     "rails": [
        { "wall": "...", "z": ..., "u0": ..., "u1": ..., "role": "sill|mid|lintel|..." }
     ],
     "braces": [
        { "wall": "...", "u0": ..., "z0": ..., "u1": ..., "z1": ..., "role": "knee_brace|..." }
     ],
     "infill_cells": [
        { "wall": "...", "u0": ..., "u1": ..., "z0": ..., "z1": ..., "shape": "rect|triA|triB" }
     ]
  }
}

IMPORTANT:

Blender must build MEMBERS.
Blender must NOT derive members from axes.

Axes are helper geometry only.
Members are authoritative construction artifacts.
