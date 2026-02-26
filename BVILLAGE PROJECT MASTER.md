# BVILLAGE — PROJECT MASTER (EARLY STAGE)

**Projekt:** bvillage  
**Phase:** frühe Baustelle / Architektur wird parallel zum Code entworfen.  
**Ziel:** historisch plausible, baubare Hausgenerierung in Blender; später Dorf/Stadt.

---

## 0. Arbeitsrealität
- Viele Module sind experimentell.
- Wir priorisieren Lernkurven, Debugbarkeit, reproduzierbare Experimente.
- Architektur wird iterativ stabilisiert.

---

## 1. Stabiler Kern (darf nicht driftet)
Diese Komponenten gelten als **STABLE** (Änderungen sind bewusst + dokumentiert):

1) **Datenmodell:** `bvillage.core.model`  
   - frozen dataclasses (StructurePlan, InteriorPlan, OpeningsPlan, Issue, …)

2) **Notes-Schema:** `bvillage.core.notes`  
   - Canonical: `notes["domains"][domain][artifact]`

3) **Registry/Plugins:** `bvillage.core.registry`  
   - type provider discovery, idempotent

4) **Logging-Konfiguration:** `bvillage.core.logging_conf`  
   - safe reload, bvillage-namespace, keine duplicate handlers

5) **Numerische Toleranzen:** `bvillage.core.geom_eps`  
   - EPS_EQ / EPS_MERGE / EPS_INSIDE sind zentral

Diese fünf sind das Fundament der Skalierbarkeit.

---

## 2. Baustellen-Zonen (dürfen brechen)
Als **EXPERIMENTAL** gelten aktuell:

- Domain-Builder (Blender): `bvillage.domains.fachwerk.blender.*`
- Domain-Core Heuristiken: `axes_*`, `openings_norm`, `frameplan`
- Typuslogik: `bvillage.types.*` (Planner/Interior/Openings/Validate)
- Roof/Infills/Timber-Profilierung

Regel: Experimentelles darf refactoren, aber muss reproduzierbar bleiben.

---

## 3. Reproduzierbarkeit (Pflicht, auch im Experiment)
Jeder relevante Versuch braucht:
- `ctx.seed`
- klare Dims/Policy
- Report oder Logs, die den Zustand erklären

Golden Reports/Tests sind der Anker.

---

## 4. Architekturgrenzen (minimal, aber hart)
1) **Core importiert kein Blender** (`bpy` verboten in core)
2) **Domain-Core importiert kein Blender**
3) **Blender baut nur aus Artefakten** (notes / Plans), keine Achsenberechnung
4) **Repairs müssen sichtbar sein** (Report + WARNING)
5) **Ordering deterministisch** (Sortierung, Naming)

---

## 5. Current Focus (aktuelle Baustelle)
- Builder schrittweise FramePlan-getrieben machen
- Tragwerk muss Öffnungen konstruktiv reflektieren
- Thin-band / Achsen-Reparaturen müssen nachvollziehbar bleiben

---

## 6. Snapshot (für neue Chats)
=== SNAPSHOT ===
- Stable core: model / notes / registry / logging_conf / geom_eps
- Active domain: fachwerk (axes_u, axes_z, frameplan, openings_norm)
- Active type: fachwerkhaus.hallenhaus
- Builder refactor: moving from axis_x raster to FramePlan axes_u truth
=== END SNAPSHOT ===


# ============================================================
# SNAPSHOT – Pre v0.2.0 Transition
# ============================================================

## Current State

- Active domain focus: Fachwerk / Langhaus
- Builder is being consolidated toward fully FramePlan-driven geometry
- Deterministic generation is required before structural interface changes
- No order system exists yet (type parameters are implicit)

---

## Next Structural Milestone

### v0.2.0 – Typed Order & Offer Interface

Status: PLANNED (deferred until Langhaus stabilization)

Purpose:

Introduce a scalable, type-specific ordering system that:

- Decouples typ-specific parameters from Context
- Enables structured presets and parameter validation
- Stores order provenance in notes
- Prepares a generic Offer interface for future city-builder logic
- Allows non-rectangular footprints (polygon-ready)

This milestone is architectural and affects provider contracts.

---

## Activation Conditions

v0.2.0 may only begin once:

- Langhaus generation is stable and deterministic
- Builder is fully FramePlan-driven
- No structural refactor is in progress
- A reproducible Langhaus reference case exists

---

## Architectural Direction

Future system must satisfy:

- Core remains type-agnostic
- Context remains environmental only
- Typ-specific parameters live exclusively in providers
- City-builder evaluates offers via metrics + tags (not parameter semantics)
- No silent parameter fallback allowed

---

---

# Plot & 3D Build Envelope Foundation

Status: PREPARATION (pre v0.2.0 groundwork)

## Motivation

The current system assumes rectangular footprints defined by:

- length
- width
- rotation

This model is insufficient for:

- polygonal parcels
- corner lots
- sloped terrain (hanglagen)
- basements
- bridges / clearance volumes
- high-rise stepback logic
- partial underground structures

To avoid a future architectural refactor, BVILLAGE introduces:

- Plot as polygonal core primitive
- 3D BuildEnvelope as constraint system

This is a foundational change and must be introduced carefully,
without breaking existing Langhaus stability.

---

## Conceptual Separation

### 1) Plot (External Reality Layer)

Represents real-world parcel constraints.

Contains:

- boundary polygon (world coordinates)
- buildable polygon (after setbacks)
- street edge indices (one or multiple)
- terrain model (plane MVP → heightmap later)

Plot is owned by SettlementBuilder.
Plot must NOT be known to Domain or Blender.

---

### 2) BuildEnvelope (Constraint Layer)

Defines allowed construction volume.

Contains:

- horizontal buildable zones (above ground)
- horizontal buildable zones (below ground)
- support zones (where load transfer is allowed)
- clearance zones (void volumes required)
- vertical rules:
  - max height
  - max depth
  - storey constraints

All special cases (basement, corner building, bridge, tower)
must be expressed through envelope constraints.

No procedural special-casing allowed.

---

### 3) BuildingVolume (Decision Layer)

Represents chosen building geometry.

Contains:

- footprint polygon (local coordinates)
- placement (world transform)
- levels (including negative values)
- optional supports
- optional void zones

Fit validation must verify:

- horizontal containment
- vertical limits
- support validity
- clearance preservation

---

## Architectural Rules

1. Domain must not depend on Plot.
2. Blender must not perform containment checks.
3. Grid remains rectangular internally (masked by footprint).
4. Terrain logic must not exist in Builder.
5. All fit violations produce Issue objects.

---

## Implementation Strategy

Phase 1 (ARC-003):
- Introduce Plot dataclass (polygon + terrain plane MVP)
- Introduce Footprint.polygon_local
- Introduce Placement abstraction
- Add deterministic polygon containment validator
- Add terrain_z() plane function
- Add Δz slope analysis helper

Phase 2 (ARC-004):
- Introduce levels abstraction (positive + negative)
- Add vertical rules
- Implement 3D envelope validator
- Define FFL heuristic (street-aligned)
- Log envelope violations as Issues

---

## Determinism Guarantee

All geometry checks must:

- use centralized EPS tolerances
- be seed-independent
- be fully deterministic
- never silently clamp

---

This foundation prepares:

- hanglage support
- basements
- corner buildings
- bridges
- towers
- future multi-domain expansion

without modifying Domain or Builder contracts.

End of snapshot.
