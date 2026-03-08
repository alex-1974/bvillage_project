# BVILLAGE_ARCHITECTURAL_ONTOLOGY.md

## Architectural Ontology of the BVILLAGE System

### Status

Normative project documentation

### Purpose

This document defines the **architectural ontology used by the BVILLAGE system**.

BVILLAGE generates historically plausible architecture through a plugin-based generative pipeline.
To support extensibility and historical accuracy, architectural knowledge is separated into clearly defined ontology layers.

These layers determine:

* where architectural terminology belongs
* how plugins interact
* how construction systems and building types are represented
* how the generator composes architecture

This document establishes the canonical ontology structure used throughout the BVILLAGE project.

---

# 1. Fundamental Architectural Principle

BVILLAGE follows a **plugin-based architecture generator model**.

The system consists of:

```text
Core Engine
    ↓
Construction System
    ↓
Structural Grammar
    ↓
Structural Archetype
    ↓
Building Archetype
    ↓
Context / Policy
```

Each layer owns a different category of knowledge.

---

# 2. Core Engine Layer

## Definition

The Core Engine provides the **execution infrastructure** of BVILLAGE.

It contains no architectural semantics.

The Core must remain **architecture-agnostic**.

### Core Neutrality Rule

The Core must function correctly even if:

* all construction systems are removed
* all archetypes are removed
* new architecture systems are added

Therefore the Core must **not define architectural terminology**.

---

## Core Responsibilities

Examples of Core concepts include:

* plugin registry
* provider interfaces
* artifact containers
* contract system
* validation framework
* policy resolution
* deterministic seed handling
* pipeline execution
* logging and reporting

Typical core terms include:

```
context
registry
plugin
provider
artifact
contract
validator
issue
policy
pipeline
trace
report
```

None of these concepts depend on a specific architecture.

---

# 3. Construction System Layer

## Definition

A **Construction System** describes the fundamental structural logic used to build a structure.

It defines the construction method and the physical structural model.

Examples include:

```
timber_frame_construction
log_construction
masonry_construction
earth_construction
mixed_construction
```

Each construction system defines:

* structural elements
* joinery systems
* load paths
* material logic
* construction grammar

---

## Example: Timber Frame Construction

Typical structural elements:

```
post
beam
brace
rail
rafter
purlin
infill_panel
```

---

## Example: Log Construction

Typical structural elements:

```
log
log_course
corner_notch
log_joint
```

These concepts belong exclusively to the log construction ontology.

---

# 4. Structural Grammar Layer

## Definition

Structural grammar describes the **rules that govern how structural elements combine**.

This layer defines the valid construction logic of a construction system.

Examples include:

* permitted connections
* allowed structural relationships
* joinery rules
* structural assembly patterns

---

## Example: Timber Frame Grammar

Example structural rules:

```
post → beam
beam → brace
post → brace
beam → rafter
```

---

## Example: Log Construction Grammar

```
log_course → log_course
log → corner_notch
```

Structural grammar is defined **inside each construction system plugin**.

---

# 5. Structural Archetype Layer

## Definition

Structural Archetypes describe recurring **structural organization patterns** within a construction system.

They define how structural elements are spatially organized.

Structural archetypes do not describe buildings themselves.

They describe **structural systems**.

---

## Examples in Timber Frame Construction

```
hall_frame
aisled_frame
cross_frame_system
multi_aisle_frame
```

These describe structural arrangements of frames.

---

## Examples in Log Construction

Possible structural archetypes may include:

```
stacked_log_structure
corner_locked_structure
multi_room_log_structure
```

---

# 6. Building Archetype Layer

## Definition

Building Archetypes describe **historically recognized building types**.

They define the spatial organization of a building.

Building archetypes rely on structural archetypes and construction systems.

---

## Important Rule

Building archetypes are **not global**.

They belong to a specific construction system.

---

## Example: Timber Frame Building Archetypes

```
hall_house
wealden_house
ernhaus
niederdeutsches_hallenhaus
ackerburger_house
mitteltennhaus
```

---

## Example: Log Construction Building Archetypes

```
log_house
blockhouse
izba
nordic_log_house
```

These building types use completely different structural ontologies.

---

# 7. Relationship Between Layers

The ontology layers form a dependency hierarchy.

```
Construction System
    ↓
Structural Grammar
    ↓
Structural Archetype
    ↓
Building Archetype
```

Formally:

```
Building Archetype ⊂ Structural Archetype ⊂ Construction System
```

---

# 8. Context / Policy Layer

The Context Layer modifies architecture based on environmental and cultural factors.

Typical parameters include:

```
region
culture
epoch
wealth
settlement_type
building_use
style
```

Policies influence:

* proportions
* materials
* details
* layout variations

Policies do not define architectural terminology.

---

# 9. Terminology Ownership

Each ontology layer owns a specific type of terminology.

| Layer                | Owns                      |
| -------------------- | ------------------------- |
| Core                 | engine terminology        |
| Construction System  | structural elements       |
| Structural Grammar   | connection rules          |
| Structural Archetype | structural layout systems |
| Building Archetype   | building types            |
| Policy               | contextual modifiers      |

---

# 10. Implications for the Code Architecture

The ontology structure determines the plugin architecture.

Example structure:

```
bvillage/

core/

construction/

    timber_frame/
        ontology/
        grammar/
        structural_archetypes/
        building_archetypes/

    log_construction/
        ontology/
        grammar/
        structural_archetypes/
        building_archetypes/

    masonry/
        ontology/
        grammar/
        structural_archetypes/
        building_archetypes/
```

Building archetypes are therefore implemented inside their construction system.

Example:

```
construction/timber_frame/building_archetypes/hall_house
```

---

# 11. Architectural Compatibility Rules

Not all combinations are valid.

Compatibility rules define allowed combinations.

Example:

```
hall_house
    requires hall_frame

hall_frame
    requires timber_frame_construction
```

---

# 12. Extensibility

This ontology model allows BVILLAGE to support architecture from different cultures and periods without changing the Core.

New architecture systems can be added simply by adding new plugins.

Examples of future expansions:

* Japanese timber architecture
* Alpine log construction
* Mediterranean stone architecture
* Roman architecture

---

# 13. Summary

BVILLAGE separates architectural knowledge into a hierarchical ontology:

```
Core Engine
Construction System
Structural Grammar
Structural Archetype
Building Archetype
Policy Context
```

The Core remains architecture-agnostic.

All architectural semantics are implemented in plugins.

This design enables BVILLAGE to generate historically plausible architecture across many construction traditions.

---
