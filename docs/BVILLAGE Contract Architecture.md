# BVILLAGE Contract Architecture & Migration Plan (Revised)

## Purpose

This document defines **where contracts belong in the BVILLAGE architecture** and how to **systematically migrate the existing codebase** to a clean contract structure.

The goals are:

* maintain architectural layer integrity
* eliminate contract duplication
* support multiple construction systems and building types
* keep the codebase stable during refactoring
* remain compatible with upcoming **architect / construction grammar restructuring**

This document intentionally avoids premature folder restructuring.

---

# 1. Core Architectural Principle

BVILLAGE follows a **layered system architecture**:

```
Engine Core
   ↓
Construction Domains
   ↓
Architectural Types
   ↓
Generators / Builders
```

Each layer may define contracts **only for concepts that belong to that layer**.

**Placement rule**

| Contract Scope | Location                    |
| -------------- | --------------------------- |
| system-wide    | `bvillage/core`             |
| domain-wide    | `bvillage/domains/<domain>` |
| type-specific  | `bvillage/types/<type>`     |

Contracts must always live at the **lowest layer where they remain valid**.

---

# 2. Core Contracts (Global Engine Contracts)

Location:

```
bvillage/core/
```

Core contracts define **engine-level artifacts** used across the entire system.

Examples:

```
Context
StructurePlan
InteriorPlan
OpeningPlan
Issue
ResolvedPolicy
```

Possible structure:

```
bvillage/core/
│
├─ model.py
│
├─ contracts/
│   structure_plan.py
│   interior_plan.py
│   openings_plan.py
│
├─ ontology/
│   structural_terms.py
│
├─ policy/
│   policy_types.py
│
└─ validation/
    validate.py
```

Important rule:

**Core must remain construction-agnostic.**

Core must **not know anything about:**

* Fachwerk
* posts
* braces
* rafters
* bays
* hallenhaus
* etc.

---

# 3. Domain Contracts (Construction System)

Location:

```
bvillage/domains/<domain>
```

Example:

```
bvillage/domains/fachwerk/
```

Domain contracts describe the **construction system**.

Example responsibilities:

* timber frame member semantics
* frame topology
* domain construction constraints
* domain validation

Example structure:

```
bvillage/domains/fachwerk/
│
├─ core/
│   contract_frameplan_fachwerk.py
│   validate_frameplan_fachwerk.py
│
├─ blender/
│   build_frame.py
│   braces.py
│   infills.py
│   opening_frames.py
│
└─ generator/
    architect.py
```

Domain contracts may define:

* `FramePlan` variants
* allowed member types
* construction rules
* domain validation logic

---

# 4. Type Contracts (Architectural Archetypes)

Location:

```
bvillage/types/<type>
```

Example:

```
bvillage/types/fachwerkhaus/hallenhaus/
```

Types define **architectural archetypes**, not construction systems.

Type contracts include:

* spatial layouts
* mandatory spaces
* typological rules
* proportional constraints

Example rules:

```
DIELE ≥ 40%
STALL ≥ 20%
```

Types may add additional validation but **must not redefine domain construction rules**.

---

# 5. Structural Ontology

Structural ontology resides in:

```
bvillage/core/ontology/
```

Example:

```
structural_terms.py
```

Ontology defines **stable semantic identifiers** used by all domains.

Examples:

```
POST_PRIMARY
BRACE_DIAGONAL
INFILL_CELL
```

These identifiers must remain globally stable.

Domains may extend the ontology but must not redefine core identifiers.

---

# 6. Validation Layers

Validation is divided into three conceptual layers.

```
validation
│
├─ schema
├─ domain
└─ physics
```

### Schema Validation

Ensures structural correctness of artifacts.

Examples:

* required fields
* schema version
* coordinate system validity

---

### Domain Validation

Ensures construction system correctness.

Examples:

* brace density
* member spacing
* construction topology

---

### Physics Validation

Ensures structural plausibility.

Examples:

* span limits
* timber capacity
* load plausibility

---

# 7. Current Problems in Repository

Several architectural issues currently exist.

### Problem 1 — Contracts appear in mixed layers

Example:

```
domains/fachwerk/core/contract_frameplan_langhaus.py
```

This mixes:

* domain rules
* type rules
* schema rules

---

### Problem 2 — Schema versions inconsistent

Example:

```
schema_version = 3
schema_version = 4
```

---

### Problem 3 — Structural ontology duplication

Multiple structural term definitions exist.

---

# 8. Migration Strategy

Migration must be **incremental and safe**.

Contracts must be stabilized **before** folder restructuring.

---

# Phase 1 — Freeze Current Behavior

Create repository snapshot.

```
git tag pre-contract-refactor
```

Run tests.

```
pytest
```

Store example artifacts (FramePlan output).

---

# Phase 2 — Ontology Consolidation

Choose canonical ontology location.

```
core/ontology/structural_terms.py
```

Remove duplicate definitions from domains.

Update imports.

---

# Phase 3 — Schema Version Unification

Search for all schema references.

```
grep -R schema_version bvillage
```

Define a single schema version.

---

# Phase 4 — Domain Contract Cleanup

Evaluate:

```
contract_frameplan_langhaus.py
```

Determine whether it belongs to:

```
domains/fachwerk
```

or

```
types/fachwerkhaus/hallenhaus
```

Move accordingly.

---

# Phase 5 — Validator Separation

Create clear validator locations.

```
core/validation/schema/
core/validation/domain/
core/validation/physics/
```

Move validators accordingly.

---

# Phase 6 — Remove Redundant Structures

Ensure single definitions for:

* Member
* FramePlan
* structural terms

---

# 9. Architect Refactor Consideration

The BVILLAGE system is currently evolving toward **construction grammar-based architects**.

Examples include:

```
StaenderbauArchitect
RaehmbauArchitect
CruckArchitect
AisledArchitect
WandrastersystemArchitect
```

These correspond to distinct **construction grammars** rather than simple building types.

Because of this architectural shift, the folder structure may need future adjustments.

---

# 10. Rule for Folder Changes

Folder restructuring must **never precede architectural clarification**.

Instead:

1. determine architectural responsibilities
2. stabilize contracts
3. then update folder structure if necessary

---

# 11. Practical Migration Rule

During the contract migration:

* **do not perform large folder renames**
* **do not move architects prematurely**
* **stabilize contracts first**

New files should only be added where their scope is already certain.

---

# 12. Future Folder Refactor Phase

After contract stabilization, a dedicated phase may evaluate folder changes.

Questions to answer:

* Are architects organized by **construction grammar** or **type**?
* Should domains contain their own architect trees?
* Should grammar modules exist inside domains?

Possible future structures may include:

```
domains/fachwerk/architects/
domains/fachwerk/grammars/
```

However, these changes must follow confirmed architectural decisions.

---

# 13. Final Target Architecture

After stabilization, the repository should approximate:

```
bvillage/

core/
    model.py
    contracts/
    ontology/
    policy/
    validation/

domains/
    fachwerk/
        core/
        blender/
        generator/

types/
    fachwerkhaus/
        hallenhaus/
```

---

# 14. Key Rule of BVILLAGE Architecture

The system hierarchy must remain:

```
Core → Domain → Type
```

Core defines the engine.
Domains define construction systems.
Types define architectural archetypes.

Contracts must always respect this hierarchy.

---

# End of Document

