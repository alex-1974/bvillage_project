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
    
1.3 Structural members are the canonical construction definition.
    - All geometry emitted by Blender must derive exclusively from:
          members = { posts, rails, braces, infills }
    - Axis data (axes_u / axes_z) is planning metadata only.
    - Axis data must never be interpreted as geometry inside Blender.

1.4 FramePlan must emit explicit members.
    - FramePlan may internally use axes for planning.
    - frameplan_to_dict() must convert planning data into members.
    - Blender must never reconstruct structure from axes.

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
7.4 Builder must never:
    - derive structure from grid
    - generate braces from axes
    - infer plates from spans
    - create structural members not present in `members`

7.5 Missing members is a contract failure.
    - Builder must abort if required members are absent.
    - No legacy fallbacks are permitted (schema_version >= 3)

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

### Naming Freeze Policy

New files and functions must follow the defined naming policy immediately.

Full repository rename is deferred to:
NR-0.4.0 (post structural stabilization window).

No mixed naming conventions allowed in new modules.

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

### Future-Proof Interface Requirement

The following interfaces must exist even if not fully active:

- Plot (external reality layer)
- InteriorPlan (semantic interior layer)
- Issue (standardized validation output)

These interfaces must not alter domain logic until explicitly activated.

This prevents architectural rewrites when expansion begins.

---

------------------------------------------------------------
13. SCHEMA VERSIONING
------------------------------------------------------------

13.1 schema_version = 3 defines the Members-Only Architecture.

13.2 For schema_version >= 3:
     - members are mandatory
     - legacy geometry paths are forbidden
     - builder fallback logic is prohibited

13.3 Structural changes require schema increment.

# Known Failure Modes (Architecture Pitfalls)

1. Builder derives posts from grid instead of FramePlan
→ causes posts through openings

2. FramePlan only stores axes, not members
→ duplication of construction logic in Blender

3. Interior modifies exterior walls directly
→ role boundary violation

4. Blender reconstructs members from axes
→ violates members-first architecture

5. FramePlan emits incomplete members
→ contract breach

These are considered architectural violations.

------------------------------------------------------------
14. POLICY AXIS SYSTEM
------------------------------------------------------------

14.1 Purpose

The policy axis system defines how house variation is structured
across time, region, construction domain, and topology.

This system exists to prevent:
    - policy explosion
    - style creep into structural logic
    - architectural rewrites after expansion
    - hidden coupling between axes

Balanced goals:
    - historical accuracy
    - combinatoric variety
    - system stability


------------------------------------------------------------
14.2 AXIS HIERARCHY
------------------------------------------------------------

Policy axes are hierarchical and orthogonal.

Primary Axes (identity-defining, structural impact):

    A) ConstructionDomain
        - defines structural grammar and load paths
        - examples: timber_frame, blockbau, masonry, earth

    B) Archetype
        - defines plan topology family
        - examples: langhaus, courtyard_house, townhouse, towerhouse

Secondary Axes (strong modulation, planning layer):

    C) TopologyModifier
        - L-form, T-form, U-form, wing additions
        - plot-reactive shape adaptations

    D) VerticalModel
        - stories count
        - attic usage
        - jetties / overhang floors

    E) RoofSystem
        - roof type
        - pitch range
        - overhang range
        - eaves height

    F) OpeningsStrategy
        - semantic opening demand
        - privacy/light bias
        - defensive bias

Tertiary Axes (contextual modulation only):

    G) StyleContext
        - region × epoch × wealth × settlement
        - may modify ranges and biases
        - must not redefine topology or construction domain

    H) Noise
        - deterministic micro-variation
        - never structural


Rule:
Lower-tier axes may modulate parameters
but must never replace or redefine higher-tier axes.


------------------------------------------------------------
14.3 POLICY STACK CONTRACT
------------------------------------------------------------

Planner must resolve policies via a stack.

Mandatory resolution flow:

    resolve_policy_stack(ctx) → ResolvedPolicy

Stack order:

    1) BaseTypePolicy
    2) TopologyModifierPolicy (optional)
    3) VerticalPolicy (optional)
    4) RoofPolicy (optional)
    5) OpeningsPolicy (optional)
    6) StylePolicy (optional)
    7) CulturePolicy (domain-specific, optional)
    8) ConstraintsPolicy (optional)
    9) NoisePolicy (optional)

All policies are patches (deltas).
None means “no modification”.

Planner must operate exclusively on ResolvedPolicy.


------------------------------------------------------------
14.4 PATCH DISCIPLINE
------------------------------------------------------------

14.4.1 Policies must not duplicate full parameter trees.

14.4.2 Policies may only override canonical parameters.

14.4.3 Unknown patch keys are forbidden.
        Attempting to patch an undefined canonical key
        must produce a HARD Issue.

14.4.4 Silent fallback behavior is forbidden.


------------------------------------------------------------
14.5 DOMAIN ISOLATION
------------------------------------------------------------

ConstructionDomain and CulturePolicy:

    - define constructive grammar
    - generate structural members
    - never read region/epoch directly
    - consume already resolved policy data only

StylePolicy must not:
    - switch construction domains
    - replace archetypes
    - inject structural members

Violation is architectural drift.


------------------------------------------------------------
14.6 SUBTYPE DISCIPLINE
------------------------------------------------------------

Subtypes must be:

    - local to a specific archetype
    OR
    - implemented as an optional patch axis

Subtypes must never become a mandatory global field.

If a requested subtype is unsupported:
    - explicit HARD or SOFT Issue must be produced
    - silent ignore is forbidden


------------------------------------------------------------
14.7 INVARIANTS
------------------------------------------------------------

ResolvedPolicy must pass invariant validation before planning.

Examples:

    - openings fit into wall segments
    - roof pitch compatible with story height
    - topology modifier produces valid footprint
    - bay counts produce non-degenerate grid

Invariant violations must be logged and deterministic.


------------------------------------------------------------
14.8 ANTI-PATTERNS (ARCHITECTURAL FAILURES)
------------------------------------------------------------

Forbidden patterns:

1) Style modifies topology directly
2) Style switches construction domain
3) Domain interprets region/epoch directly
4) Planner contains hidden structural defaults
5) Axes silently ignored

These patterns cause long-term architectural instability
and are considered violations of the system contract.


------------------------------------------------------------
14.9 EXPANSION RULE
------------------------------------------------------------

New axes may be added only as optional patch slots.

Default must be neutral (no effect).

Adding a new axis must not require modification
of existing archetypes or domains.

Structural grammar changes require:
    - new ConstructionDomain
    OR
    - new CulturePolicy branch
    OR
    - schema version increment
