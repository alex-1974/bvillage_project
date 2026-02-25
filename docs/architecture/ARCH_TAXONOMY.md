# BVILLAGE Architectural Taxonomy
Version: 0.1
Status: Foundational Document
Scope: Long-term historically grounded classification framework

---

# 1. Purpose

BVILLAGE separates architectural knowledge from generation logic.

This document defines the classification system used to describe
and extend building types across regions and epochs.

The taxonomy is research-driven and expandable.

---

# 2. Core Classification Axes

Buildings are defined along three primary axes:

## 2.1 Construction Domain (Bauweise)

Defines structural logic and load-bearing system.

Examples:
- fachwerk
- mauerwerk
- blockbau
- hybrid

Domain controls:
- structural behavior
- material usage logic
- load paths
- frame generation
- compatibility with PhysicalPlausibilityValidator

---

## 2.2 Topological Archetype

Defines spatial organization and building logic.

Examples:
- Hallenhaus
- Ernhaus
- Stadthaus
- Speicher
- Hofanlage
- Ackerbürgerhaus

Archetypes define:
- spatial program
- circulation logic
- opening requirements
- geometric intent
- typical span ranges (not fixed dimensions)

Archetypes do NOT define final beam sections.

---

## 2.3 Style / Context Policy

Modulates domain and archetype without redefining topology.

Parameters:
- Region
- Epoch
- Wealth
- Urban / Rural
- Climate

Influences:
- material selection
- parameter ranges
- roof pitch
- window density
- ornament level
- construction culture behavior

---

# 3. Fachwerk Topology Table (Research Base)

| ID | Name | Signature | Region | Period |
|----|------|----------|--------|--------|
| FW-LH-ND | Niederdeutsches Hallenhaus | Längsdiele, dreischiffig | Norddeutschland | 13–19 Jh |
| FW-LH-2S | Hallenhaus Zweiständer | 2 Innenständerreihen | Norddeutschland | 15–18 Jh |
| FW-LH-3S | Hallenhaus Dreiständer | asymmetrische Ständer | Norddeutschland | 16–18 Jh |
| FW-LH-4S | Hallenhaus Vierständer | 4 Ständerreihen | Norddeutschland | 16–19 Jh |
| FW-ER-MD | Mitteldeutsches Ernhaus | Querflur (Ern) | Mittel-/Süddeutschland | 14–18 Jh |
| FW-HARZ | Harzer Haus | Ernhaus-Variante | Harz | 16–19 Jh |
| FW-UMG | Umgebindehaus | Blockstube + Umgebinde | Oberlausitz | 15–19 Jh |
| FW-GULF | Gulfhaus | Großraum (Gulf) | Nordseeküste | 16–19 Jh |
| FW-HAUB | Haubarg | Zentralständer-Großbau | Nordfriesland | 17–19 Jh |
| FW-MITT | Mittertennhaus | Tenn zentral | Alpenraum | 15–19 Jh |
| FW-STG-GIE | Giebelständiges Stadthaus | schmale Parzelle | Städte | 14–18 Jh |
| FW-STG-TRF | Traufenständiges Stadthaus | Traufe zur Straße | Städte | 15–18 Jh |
| FW-ACK | Ackerbürgerhaus | Stadt + Wirtschaft | Kleinstädte | 15–19 Jh |
| FW-SPC | Speicherhaus | Lagerbau | Städte | 15–18 Jh |
| FW-HOF | Fachwerk-Hofanlage | Mehrflügelanlage | Mittel-/Süddeutschland | 16–19 Jh |

This table is expandable and research-driven.

---

# 4. Structural Realism Separation

BVILLAGE separates:

## 4.1 PhysicalPlausibilityValidator (Timeless Physics)

- structural mechanics
- load checks
- deflection
- material strength

Answers:
"Would it physically hold?"

---

## 4.2 ConstructionCulturePolicy (Historical Behavior)

Defines how close to physical limits builders operated.

Parameters:
- max_utilization_ratio
- redundancy_preference
- overdimension_factor
- support_density_preference

Answers:
"Would builders of this period likely build it that way?"

This creates epoch-specific structural character.

---

# 5. Material Dimension (Cross-Cutting Layer)

MaterialRegistry provides:

A) Physics parameters
- E-modulus
- density
- allowable strengths

Used by:
PhysicalPlausibilityValidator

B) RenderProfile
- base_color_hex
- roughness
- metallic
- deterministic variation palette

Used by:
Blender material adapter

Important:
Physics and visual parameters must remain independent.

---

# 6. Structural Dimension Resolution Pipeline

1. Archetype defines geometric span intent.
2. Domain defines structural system.
3. Physics computes minimal required section.
4. ConstructionCulturePolicy modifies sizing.
5. PhysicalPlausibilityValidator verifies final structure.
6. Evaluator selects best candidate.

---

# 7. Scalability

This taxonomy supports:

- 50+ archetypes
- multiple domains
- unlimited regional expansion
- multi-epoch differentiation

The engine remains stable.
Knowledge grows via taxonomy and policy layers.

---

# 8. Determinism

All variation must be seed-based.

world_seed + settlement_seed + house_salt

Ensures:
- reproducibility
- debuggability
- controlled diversity
