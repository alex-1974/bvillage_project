# BVILLAGE – System Concepts

---
tier: 1
authority: CANONICAL
change-frequency: low
change-rule: Change only when the conceptual model changes. Implementation detail does not belong here.
referenced-by: SYS_CONTRACT.md, ARCH_POLICIES.md, ARCH_TAXONOMY.md, ARCH_MATERIALS.md
references: SYS_PRINCIPLES.md
---

This document describes the conceptual model of BVILLAGE — what the system is, how it thinks, how its parts work together. It assumes the principles in SYS_PRINCIPLES.md and explains how they translate into a concrete system model.

The current implementation covers medieval central European timber framing. The examples in this document reflect that starting point. The model itself is not limited to it.

---

## 1. The three axes

Every building in BVILLAGE is defined along three primary axes. They are independent of one another and answer different questions.

**Construction domain** answers: how does the building stand? It defines the structural grammar — which members are generated, how loads flow, which joinery or bonding types are possible. Timber frame, log construction, masonry, rammed earth, and steel frame are different domains. Each generates different members, has different validation rules, different material constraints. Switching domain is not a style operation — it is a structural break.

**Topological archetype** answers: how is the building organized? It defines spatial logic — zones, circulation, opening requirements, geometric intent. Two buildings with the same construction domain but different spatial organization are different archetypes. A longhouse and a courtyard house may both be timber-framed — they are not the same archetype. Conversely, the same archetype in two different regions remains the same archetype; what changes is the policy that shapes it.

**Style and context policy** answers: in what context does the building stand? It modulates — region, epoch, wealth, urban or rural setting, climate. It adjusts parameter ranges, material selection, roof pitches, window densities, ornament levels. It does not change topology. It does not switch domain.

These three axes are orthogonal. Knowledge belonging to one axis must never migrate to another.

---

## 2. The policy system

Policies are the mechanism through which the system scales. Without them, every new combination of region, epoch, culture, and type would have to be encoded in the planner — making the system unmanageable by the third or fourth extension. With policies, every new historical or cultural insight enters as a new configuration, without touching the core.

The same engine that generates a fourteenth-century north German Hallenhaus can generate a seventeenth-century Anatolian courtyard house — different domains, different archetypes, different policies, same pipeline.

### What policies are

Policies are parameter packages that the planner receives from outside. They do not tell the planner how to plan — they tell it with which values to plan. The planner receives a resolved policy. It does not ask where it came from.

Each policy layer is a delta — a set of overrides on a canonical parameter tree. Layers that contribute nothing are empty. Empty layers change nothing.

### The policy stack

Policies resolve in a defined stack, from generic to specific:

1. **BaseTypePolicy** — the archetype's defaults. What holds when no context is known?
2. **TopologyModifierPolicy** — optional footprint modifications: L-form, T-form, U-form.
3. **VerticalPolicy** — storey count, attic use, cantilevered floors.
4. **RoofPolicy** — roof type, pitch ranges, eaves heights.
5. **OpeningsPolicy** — opening demands, light and privacy preferences.
6. **StylePolicy** — region × epoch × wealth × settlement type.
7. **CulturePolicy** — domain-specific construction culture: member spacing, structural grammar, infill logic.
8. **ConstraintsPolicy** — hard and soft constraints with deviation cost weights.
9. **NoisePolicy** — deterministic micro-variation within allowed bands.

Later layers can override earlier ones. No layer may operate outside its domain of responsibility.

### What policies may not do

StylePolicy may not switch construction domain and may not replace an archetype. It modulates — it does not redefine. If a regional variation requires a different structural grammar, that is a new domain or a new CulturePolicy branch, not a StylePolicy variant.

CulturePolicy and domain do not read region and epoch directly. They consume already-resolved policy data. What "northern Germany, sixteenth century" or "Ottoman Anatolia, seventeenth century" means has already been processed by StylePolicy before the domain sees it.

### Expansion rule

New axes enter as optional patch slots. The default is neutral — no effect. Existing archetypes and domains require no modification when a new axis is added. If adding a new axis would require changes to existing code, that is a design failure, not a feature.

---

## 3. The generation pipeline

A building emerges through an ordered pipeline of roles. Each role has a defined responsibility and a defined boundary.

**SettlementBuilder** decides which house is built where. It produces a HouseRequest with archetype ID, constraints, seed, and context. It makes no constructive decisions.

**TypePlanner** translates the HouseRequest into a semantic plan: axis grid, wall definitions, zones, opening demands. It generates no structural members. It knows how a building type is spatially organized — not how it structurally stands.

**InteriorPlanner** resolves the interior spatial organization: hearth or furnace, partitions, furniture, interior openings. It communicates with the TypePlanner through opening demands, but never touches the FramePlan directly.

**DomainConstructor** translates the semantic plan into constructive truth. It generates the FramePlan with explicit members. Structural reality is created here.

**PhysicalPlausibilityValidator** checks universal physics: would this structure hold? It operates on timeless mechanical principles, independent of epoch, region, or construction culture.

**ConstructionCulturePolicy** defines historical plausibility: would builders of this time, place, and tradition actually have built this way? It is not a validator — it is a policy that feeds the DomainConstructor, shaping member dimensions, spacing, and redundancy before they are generated. The PhysicalPlausibilityValidator checks whether the result holds; CulturePolicy determines what gets built in the first place.

**Evaluator / Orchestrator** scores candidates and selects. It changes no geometry, repairs no structure.

---

## 4. Structural truth and the members model

The FramePlan contains explicit members: discrete, named, positioned, role-assigned building elements. In a timber-framed building these are posts, rails, braces, and infill cells. In a masonry building they are courses, lintels, and piers. The abstraction is the same; the vocabulary differs by domain.

Axes (axes_u, axes_z) are planning metadata. They help the DomainConstructor place members. They are not geometry. The renderer sees axes as reference information — it builds members.

This distinction is absolute. A renderer that derives elements from axes instead of reading the members list violates the contract — even if the result looks identical by coincidence. The violation is not in the output, it is in the mechanism.

---

## 5. Physics and construction culture

The system separates two kinds of structural knowledge that are often conflated.

**Universal physics** always applies. Bending stiffness, slenderness, bearing, compression — these laws know no epoch and no culture. The PhysicalPlausibilityValidator checks them.

**Construction culture** is historical and regional. How close to the physical limit did builders of a given time and place actually operate? How much did they overdimension? Which spans were common in their tradition, which were not? What did their available tools and joinery techniques enable or prevent? The ConstructionCulturePolicy answers these questions.

Without this separation, the system produces anachronistically optimized buildings — structures that pass physics but are historically impossible. A medieval carpenter, a Roman engineer, and a nineteenth-century builder all operated within the same physics. They produced radically different structures because they worked within different cultural and technical constraints.

---

## 6. Materials

Materials serve two independent roles in the system. These roles must not be mixed.

As a **physical foundation**, materials provide the mechanical parameters — modulus, density, allowable stresses — for the PhysicalPlausibilityValidator and the DomainConstructor.

As a **visual basis**, materials provide color palettes, roughness values, and deterministic variation parameters for the renderer.

Physical values must not be changed for visual reasons. Visual values must not be changed for physical reasons. Both roles are linked through the same material identifier — the registry is the single source of truth for both.

---

## 7. Determinism

Determinism is not a technical property — it is a functional requirement. A non-deterministic system cannot be debugged, tested, or reproduced.

Every variation in the system is seed-based. The seed is composed of world_seed, settlement_seed, and house_salt. The same combination always produces the same building. Orderings are explicit and stable. No module calls a global random number generator.
