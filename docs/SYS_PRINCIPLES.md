# BVILLAGE – System Principles

---
tier: 1
authority: CANONICAL
change-frequency: rare
change-rule: Change only on fundamental directional shift. Requires CHANGELOG entry.
referenced-by: all documents
references: —
---

BVILLAGE is a deterministic architectural generation engine. It produces historically plausible buildings from any culture, region, and epoch — deterministically, physically consistently, scalable from single houses to city-scale simulation.

The system starts with medieval central European timber framing. That is the first domain, the first set of archetypes, the first body of construction culture. It is not the boundary. The same engine can represent a Mesopotamian mud-brick house, a Roman insula, a Japanese post-and-beam structure, or a nineteenth-century masonry tenement. Different domains, different policies, different knowledge — same architecture.

This document records the decisions that are no longer up for debate. It contains no implementation detail and no roadmap. It explains not just what the system does, but why it does it that way.

---

## 1. Members define structural truth

Every building, regardless of construction system, consists of discrete physical elements that carry loads, bound spaces, and frame openings. In timber framing these are posts, rails, braces, and infill panels. In masonry they are courses, lintels, and piers. In log construction they are stacked members and corner joints. The names differ. The principle does not.

The FramePlan contains explicit members. The renderer constructs exactly those members — no more, no less. It does not derive members from axes, does not invent missing elements, does not repair incomplete plans. What is in the FramePlan gets built. What is not in the FramePlan does not exist.

The reason is concrete: if the renderer makes structural decisions — even small, seemingly obvious ones — there are two sources of truth. Elements appear in wrong positions. Geometry becomes unreproducible. The members-only architecture eliminates this class of errors entirely. Structural truth lives in exactly one place.

---

## 2. The renderer renders — it does not decide

The renderer receives a complete FramePlan and builds it. It computes no axes, closes no gaps, makes no structural decisions. It is an emitter — precise, deterministic, without its own intelligence about the building.

This is not a technical limitation. It is an architectural decision. As soon as the renderer starts interpreting structure, constructive logic leaves the layer where it can be tested, validated, and versioned. Structural intelligence belongs in domain-core, not in the renderer.

---

## 3. Layers have strict boundaries

The system is divided into layers with clearly defined responsibilities that must not be crossed.

The **archetype** defines topology — the spatial organization of a building type, its zones, its circulation logic, its opening requirements. It does not define beam sections, materials, or regional characteristics.

The **construction domain** defines structural logic — how a building stands, how loads flow, which members are generated. It does not read region or epoch directly. It consumes already-resolved policy data.

**Policies** carry context-specific knowledge — what a planner needs to know about region, epoch, wealth, and intended use. They modulate parameters without changing the planning logic itself.

**The renderer** renders. It makes no decisions about what it renders.

These boundaries are non-negotiable. A system that mixes layers works initially — but it does not scale. Every new region, every new epoch, every new house type then requires intervention in the core. The goal is a system that grows without being rebuilt.

---

## 4. The planner is generic — policies are specific

A domain planner builds houses of its construction type. Which house it builds — from which epoch, which region, which culture, for which purpose — policies determine. The planner carries no embedded knowledge of geography, time, or social context.

This is the heart of the system's scalability. If regional, epochal, or typological assumptions enter the planner, every new combination either needs its own planner or adds branching that grows harder to maintain with each extension. With policies, every new historical or cultural insight enters as a new policy configuration, without touching the core.

Whether a single domain planner suffices for all variants of that domain is an empirical question that practice will answer. What is not empirical: regional, epochal, cultural, and stylistic assumptions do not belong in the planner.

---

## 5. Variation is deterministic

Same seed, same policy produces the same result — always. This is not a simplification. It is a functional requirement. A system that produces different outputs from identical inputs cannot be debugged, tested, or reproduced.

Variation comes from controlled, seed-based sampling within defined parameter ranges. No global random number generator, no hidden randomness, no ordering dependencies from unordered data structures.

---

## 6. Physics is universal — construction culture is historical

Mechanics always apply. A beam with a given cross-section carries a given load — that holds in the thirteenth century as much as today. The Inspector (`validate_physics.py`) checks exactly this: would this structure physically hold?

How close to the physical limit builders of a given epoch and region actually operated is historical and cultural. The ConstructionCulturePolicy carries this knowledge: how much did they overdimension? What redundancy did they prefer? Which spans were common in their tradition, which were not? This layer prevents anachronistic optimization — a medieval house dimensioned like a modern engineered structure is historically wrong, even if it passes physics.

---

## 7. The system may be incomplete — it may not be inconsistent

Not all house types need to exist today. Not all policies need to be fully specified. Not all validators need to be enforced.

What is not tolerated: contradictions between layers, implicit assumptions in code, silent fallbacks, two sources of truth for the same information. Inconsistency is more expensive than incompleteness, because it is invisible and accumulates.
