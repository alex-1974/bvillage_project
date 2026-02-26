# BVILLAGE

BVILLAGE is a deterministic architectural generation engine.

It generates historically plausible buildings using a strictly layered
system design and a members-first structural model.

------------------------------------------------------------------------

# 1. What This Project Is

BVILLAGE is not a mesh generator.

It is a structured engine that:

-   Separates topology, structure, policy and rendering
-   Uses deterministic seeds
-   Enforces strict layer boundaries
-   Treats structural members as canonical truth
-   Allows long-term architectural evolution without rewrites

The Blender layer is a renderer. The engine defines structural truth.

------------------------------------------------------------------------

# 2. Conceptual Separation

This project distinguishes clearly between:

## A) System Design (Software)

Defines:

-   Layer boundaries
-   Contracts
-   Determinism
-   Schema versioning
-   Builder rules
-   Validation model

Located in:

docs/sys/

------------------------------------------------------------------------

## B) Built Form (Architectural Logic)

Defines:

-   Archetypes
-   Construction domains
-   Structural grammar
-   Policy axis taxonomy
-   Generation model

Located in:

docs/built_form/

------------------------------------------------------------------------

## C) Development & Evolution

Defines:

-   Roadmap
-   Strategic milestones
-   Version progression

Located in:

docs/dev/

------------------------------------------------------------------------

# 3. Documentation Structure

docs/ sys/ → System design & contracts built_form/ → Architectural
taxonomy & generation theory dev/ → Roadmap & evolution materials/ →
Material system

------------------------------------------------------------------------

# 4. Core Principles

-   Physics is universal.
-   Construction culture is historical.
-   Archetypes define topology, not dimensions.
-   Domains define structure, not style.
-   Structural members are canonical truth.
-   Blender must never derive structure.
-   Variation must be deterministic.
-   No silent fallback logic.

------------------------------------------------------------------------

# 5. Current System Status

Members-only architecture active. Schema version ≥ 3. Blender is pure
renderer. No structural inference in Blender.

------------------------------------------------------------------------

# 6. Entry Points

New contributor:

1.  Read docs/sys/SYS_FOUNDATION.md
2.  Then docs/sys/SYS_CONTRACT.md
3.  Then docs/built_form/GENERATION_MODEL.md

Development planning:

-   See docs/dev/DEV_ROADMAP.md

------------------------------------------------------------------------

# 7. Philosophy

The project is allowed to be incomplete. It is not allowed to be
inconsistent.

Architectural stability is more important than feature speed.
