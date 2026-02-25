# BVILLAGE – ARCHITECTURE RULES
Status: ACTIVE
Scope: Engine-wide

These rules exist to prevent architectural drift during experimental development.
They are intentionally strict and minimal.

------------------------------------------------------------
1. STRUCTURAL TRUTH
------------------------------------------------------------

1.1 FramePlan defines structural truth.
    - Posts, beams, roof geometry must derive from FramePlan data.
    - Grid (axis_x / axis_y) is not structural truth.

1.2 Blender layer must not compute axes.
    - No U/Z axis generation inside any blender module.
    - Blender consumes, never decides.

------------------------------------------------------------
2. LAYER BOUNDARIES
------------------------------------------------------------

2.1 Core must never import Blender (bpy).
2.2 Domain-core must never import Blender.
2.3 Type modules must not contain Blender code.
2.4 Blender modules may import domain artifacts but must not mutate them.

------------------------------------------------------------
3. DATA MODEL DISCIPLINE
------------------------------------------------------------

3.1 Core dataclasses are frozen and immutable.
3.2 No mutation of StructurePlan, InteriorPlan, OpeningsPlan.
3.3 Domain artifacts must be stored via:
        notes["domains"][domain][artifact]

3.4 Legacy aliases are transitional only.

------------------------------------------------------------
4. DETERMINISM
------------------------------------------------------------

4.1 Same seed + same policy ⇒ identical result.
4.2 All ordering must be explicit and deterministic.
4.3 No reliance on unordered dict iteration.
4.4 Random must use local RNG seeded from ctx.seed.

------------------------------------------------------------
5. NUMERICAL STABILITY
------------------------------------------------------------

5.1 All float tolerances are centralized in geom_eps.
5.2 No ad-hoc epsilon values outside geom_eps.
5.3 Repairs must not silently change geometry.

------------------------------------------------------------
6. REPAIR POLICY
------------------------------------------------------------

6.1 Any geometry repair must:
    - be logged (WARNING)
    - appear in planner report
    - be deterministic

6.2 Silent clamping is forbidden.

------------------------------------------------------------
7. BUILDER CONTRACT
------------------------------------------------------------

7.1 Builder is a geometry emitter only.
7.2 Builder must not:
    - reinterpret dimensions
    - infer missing axes
    - override structural decisions
7.3 Builder may:
    - transform artifact data into mesh
    - create collections
    - assign materials

------------------------------------------------------------
8. VALIDATION
------------------------------------------------------------

8.1 Core validation remains type-agnostic.
8.2 Type-specific validation stays inside type modules.
8.3 Validation must not exist inside Blender modules.

------------------------------------------------------------
9. TESTS DEFINE CONTRACTS
------------------------------------------------------------

9.1 If a test encodes behavior, that behavior is part of the contract.
9.2 Golden reports must not change without documented reason.
9.3 Structural changes require new repro cases.

------------------------------------------------------------
10. EXPERIMENTATION ZONE
------------------------------------------------------------

Allowed to change freely:
- Domain heuristics
- Policy tuning
- Interior layout logic
- Roof detailing
- Infills

Not allowed to change freely:
- Layer boundaries
- Notes schema
- Determinism guarantees
- Logging discipline

------------------------------------------------------------
11. FILE IDENTITY RULE
------------------------------------------------------------

11.1 Every .py file must declare its canonical project path 
     in the very first line as a comment.

Example:

# bvillage/domains/fachwerk/blender/roof.py

11.2 The path must match the repository structure exactly.

11.3 This comment must always be the first line in the file.

11.4 This rule exists to:
     - prevent ambiguity during refactors
     - help static review
     - support AI-assisted development
     - avoid duplicate or misplaced modules

11.5 No docstring may appear before this path comment.

------------------------------------------------------------
12. NAMING CONVENTION
------------------------------------------------------------

12.1 File names must express:
     - role (planner / builder / contract / policy / quality)
     - aspect (frameplan / openings / braces / geometry / order)

12.2 Generic module names are forbidden:
     - validate.py
     - check.py
     - utils.py (without domain qualifier)

12.3 Pattern:
     <role>_<aspect>.py

12.4 Function names must follow:
     <verb>_<object>_<qualifier>()

12.5 Verb meanings:
     build_*      → emits geometry
     derive_*     → computes data
     normalize_*  → transforms data
     audit_*      → returns report (no raise)
     assert_*     → enforces invariant (may raise)

12.6 Naming must reflect architectural layer:
     - core: no Blender terms
     - blender: no constructive inference terms

Naming is part of architectural stability.

# Structural Interface Separation

BVILLAGE enforces strict separation between:

A) Structure (semantic)
B) FramePlan (constructive)
C) Blender geometry (visual)

Structure:
- rooms
- walls
- openings as demands
- semantic zones

FramePlan:
- constructive truth
- structural members
- bracing rules
- support logic

Blender:
- builds exact members
- applies materials
- no structural decisions

---

# Known Failure Modes (Architecture Pitfalls)

1. Builder derives posts from grid instead of FramePlan
→ causes posts through openings

2. FramePlan only stores axes, not members
→ duplication of construction logic in Blender

3. Interior modifies exterior walls directly
→ role boundary violation

These are considered architectural violations.
