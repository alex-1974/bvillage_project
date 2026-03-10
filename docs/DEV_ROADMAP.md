# BVILLAGE – Development Roadmap

tier: 3  
authority: OPERATIONAL  
change-frequency: frequent  
change-rule: Contains only tasks and milestones. No architectural principles.  
referenced-by: —  
references: SYS_PRINCIPLES.md, SYS_CONTRACT.md, DOCS_INDEX.md  

---

# HOW TO READ THIS DOCUMENT

This roadmap defines the operational development trajectory of BVILLAGE.

Levels:

v0.4.0 — First house + architectural foundation  
v0.4.x — Structural intelligence and policy weaving  
v0.5.0 — Second archetype (Stadthaus)  
Vision — Long-term architecture

The roadmap is a living engineering document.  
Research findings and architectural discoveries may change priorities.

---

# COMPLETED

## ARC-000 — Members-Only Architecture

Status: DONE  
Version: v0.3.0

Delivered:

- builder fully members-driven
- no axis-derived geometry
- no structural fallbacks
- deterministic generation preserved

Result:

FramePlan.members is the canonical structural truth.

---

## ENG-003 — Naming Atomic Commit

Status: DONE

Delivered:

- consistent terminology
- explicit structural field names
- removal of legacy classes

Result:

All public names are self-describing.

---

## SYS-005 — Structural Member Ontology (TID System)

Status: DONE

Delivered:

Structural members identified via canonical identifiers:

post.primary  
beam.tie  
brace.diagonal  

Result:

Stable semantic layer between Frame Producer and Renderer.

---

## CONTRACT-001 — Contract Inventory

Status: DONE

Delivered:

- full system contract inventory
- contract ownership map

Result:

Implicit contracts removed.

---

## CONTRACT-002 — Contract Matrix

Status: DONE

Delivered:

CONTRACT_MATRIX.md

Result:

Full contract transparency across the system.

---

## CONTRACT-003 — Contract Layer Separation

Status: DONE

Delivered separation of contracts into:

- core contracts
- domain contracts
- type contracts

Result:

Contracts now mirror system layering.

---

## SYS-012 — Core De-Architecturization

Status: DONE  
Version: v0.4.0

Delivered:

Removed legacy archetype schema modules:

schema_archetypes.py  
schema_archetype_bindings.py  
schema_archetype_id.py  

Archetype knowledge moved entirely into plugin layer.

Result:

Core now contains **no archetype knowledge**.

---

## SYS-013 — Plugin Discovery & Self-Registration

Status: DONE

Delivered:

- automatic plugin discovery
- dynamic module loading via `pkgutil.walk_packages`
- plugins self-register via `register()` functions

Bootstrap:

ensure_plugins_loaded()

Result:

Core contains **no static archetype tables**.

---

## SYS-014 — Construction Grammar Dispatch

Status: DONE

Delivered separation:

Archetype → topology logic  
Construction grammar → structural logic  

Example:

BOX_FRAME → BoxFrameForeman

Result:

Structural behavior determined by grammar, not archetype.

---

## CONTRACT-004 — RoofPlan Contract

Status: DONE

Delivered:

schema_roofplan_timber_frame.py  
validate_roofplan_timber_frame.py  
derive_roofplan_boxframe.py  

Result:

Roof generation defined via validated artifact:

RoofPlan

---

## SYS-015 — Pipeline Role Architecture

Status: DONE

Delivered:

BVILLAGE_PIPELINE_ROLES.md

Defines canonical roles:

SiteManager  
Foreman  
Topology Planner  
Frame Producer  
Roof Producer  
Joiner  
Inspector  
Appraiser  

Result:

Pipeline responsibilities are formally defined.

---

## SYS-016 — Policy Layer Architecture

Status: DONE

Delivered:

BVILLAGE_Policy_Layers.md

Defines the canonical ten-layer PolicyStack.

---

# v0.4.0 — First House + Foundation

Goal:

A deterministic **Hallenhaus** emerges through the full pipeline and renders in Blender.

Scope:

- structural plausibility
- deterministic generation
- policy-driven parameters
- members-only rendering

Out of scope:

- material simulation
- settlement generation
- physics gating

---

# ACTIVE WORK

## RES-001 — Historical Research

Status: ACTIVE  
Priority: CRITICAL

Research questions:

- regional construction culture
- bracing patterns
- roof construction
- structural spans
- influence of building function

Deliverable:

Documented hypotheses mapped to policy axes.

---

## HOUSE-001 — Hallenhaus through Full Pipeline

Status: ACTIVE  
Priority: HIGH

Goal:

Generate a plausible Hallenhaus visible in Blender.

Pipeline:

Context  
→ SiteManager  
→ Foreman  
→ Topology Planner  
→ Frame Producer  
→ Roof Producer  
→ Joiner  
→ Inspector  
→ Renderer  

---

## ARC-001 — PolicyStack Integration

Status: ACTIVE  
Priority: HIGH

Goal:

Remove remaining parallel policy logic.

Tasks:

- remove `_hallenhaus_policy()`
- replace with `resolve_policy_stack(ctx)`
- populate FramePolicy from ResolvedPolicy
- verify deterministic behavior

---

## ARC-001A — PolicyStack Foundation

Status: ACTIVE  
Priority: CRITICAL

Tasks:

- planner uses ResolvedPolicy only
- hard error for unknown policy keys
- invariant validation hook
- policy diagnostic reporting

---

## INT-001 — Joiner Integration

Status: ACTIVE  
Priority: HIGH

Goal:

Determine final pipeline integration for InteriorPlan.

Tasks:

- define planner ↔ joiner contract
- ensure joiner cannot mutate FramePlan
- document final pipeline order

---

## QLT-001 — Issue Schema Standardization

Status: ACTIVE  
Priority: HIGH

Goal:

Unified Issue object:

Issue  
severity  
code  
message  
location  

---

## PPV-001 — Physical Plausibility Validator

Status: PLANNED  
Priority: MEDIUM

Goal:

Physics validator runs but does not block build.

Tasks:

- integrate PPV into pipeline
- produce validation report
- ensure validator does not modify geometry

---

# v0.4.x — Structural Intelligence

Purpose:

Prepare system for second archetype.

Key tasks:

SYS-001 Policy axes implementation  
SYS-002 type-agnostic pipeline  
SYS-003 FramePlan multi-storey schema  
ROL-002 Foreman implementation  
ROL-003 role implementations  

Architecture milestone:

CR-2 — Architecture Stable

Reached when:

- PolicyStack supports multiple archetypes
- pipeline becomes type-agnostic
- Foreman coordination is complete
- FramePlan schema extended

---

# v0.5.0 — Second House

Goal:

Generate **Fachwerk Stadthaus** through the same pipeline.

Success condition:

No structural rewrites required.

---

# Vision

Future architectural layers:

CultureMap  
EcoMap  
Plot system  
Settlement generation  
Material ecology  

---

# CURRENT PROJECT STATUS

Estimated progress:

v0.4.0

≈ 80–85 %

Remaining key tasks:

- PolicyStack integration
- Joiner pipeline integration
- Issue schema finalization
- Physical plausibility validator
