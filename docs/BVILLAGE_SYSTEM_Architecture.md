# BVILLAGE System Architecture Reference

## Zweck

Dieses Dokument beschreibt die verbindliche Zielarchitektur von BVILLAGE.

Es dient als Referenz für:

- neue Features
- Refactorings
- Plugin-Integration
- Audit-Regeln
- Code Reviews

Wenn Code und dieses Dokument einander widersprechen, ist die Architektur zu prüfen und der Widerspruch bewusst aufzulösen.

---

## Grundprinzip

BVILLAGE ist eine pluginfähige Generierungs-Engine für historisch plausible Bauwerke.

Die Architektur trennt strikt zwischen:

- generischer Infrastruktur
- typologischer Planung
- baugrammatischer Ableitung
- Rendering

---

## Layer

### Core

`bvillage/core/`

Core enthält nur generische Infrastruktur.

Core darf enthalten:

- `Context`
- Dispatch / Registry
- Plugin-Bootstrap
- generische Fehler / Validation-Primitiven
- generische Policy-Container
- Artefakttransport

Core darf **nicht** enthalten:

- konkrete Archetypen
- konkrete Baugrammatiken
- konkrete Hausformen
- konkrete Domain-Policies
- Blender-Bauwissen

Core kennt keine Inhalte wie:

- `FW-LH-ND`
- `longhouse`
- `BOX_FRAME`
- `fachwerk.*`

Core kennt nur IDs und registrierte Topology Planner / Foremen.

---

### Types

`bvillage/types/...`

Types definieren Archetypen.

Types sind zuständig für:

- Topologie
- Raumlogik
- Öffnungsbedarf
- typologische Varianten
- archetypspezifische Policy-Auflösung

Types dürfen erzeugen:

- `SemanticPlan` (inkl. `OpeningsPlan` als Phase)
- `InteriorPlan`

Types dürfen **nicht** erzeugen:

- `FramePlan.members`
- `RoofPlan.members`
- Blender-Geometrie

Types registrieren sich selbst per Plugin-Mechanismus.

---

### Domains

`bvillage/domains/...`

Domains definieren Baugrammatiken.

Domains sind zuständig für:

- strukturelle Ableitung
- Frame Producer
- Roof Producer
- Domain-Contracts
- Domain-spezifische Validierung

Domains dürfen erzeugen:

- `FramePlan`
- `RoofPlan`

Domains dürfen **nicht**:

- Topologie-Archetypen definieren
- Blender-spezifische Inferenzlogik enthalten

---

### Renderer

`bvillage/blender/...`
`bvillage/domains/*/blender/...`

Renderer konsumieren fertige Artefakte.

Renderer dürfen:

- Blender-Objekte erzeugen
- Materialien zuweisen
- Profile extrudieren
- Collections organisieren

Renderer dürfen **nicht**:

- Struktur aus Achsen ableiten
- fehlende Members erfinden
- Dachlogik oder Frame-Logik nachberechnen

Renderer sind reine Emitter.

---

## Artefakte

### SemanticPlan

Wird vom Type-Layer (Topology Planner) erzeugt.

Beschreibt:

- Grundriss
- Raster
- Wände
- Felder
- Frames
- Zonen
- Räume

Enthält `OpeningsPlan` als Phase:

- Türpositionen
- Fensterpositionen
- Torpositionen

Keine strukturellen Members.

---

### InteriorPlan

Wird vom Type-Layer (Joiner) erzeugt.

Beschreibt:

- Raumlogik
- Öffnungsbedarf
- Innenbeziehungen
- Türen / Raumanforderungen

Keine strukturellen Members.

---

### FramePlan

Wird vom Domain-Layer erzeugt.

Beschreibt die strukturelle Wahrheit des Tragwerks.

`FramePlan.members` ist die verbindliche Quelle für:

- posts
- rails
- braces
- infills
- opening frames

Renderer dürfen Struktur nur aus `FramePlan` lesen.

---

### RoofPlan

Wird vom Domain-Layer erzeugt.

Beschreibt die strukturelle Wahrheit des Daches.

`RoofPlan.members` ist die verbindliche Quelle für:

- ridge
- rafters
- collar_ties
- weitere Dachträger

Renderer dürfen Dachstruktur nur aus `RoofPlan` lesen.

---

## Rollen

### Commissioner

Core-Einstiegspunkt.

Verantwortlich für:

- Archetype-ID, Seeds, Plot-Constraints
- Policy-Stack-Auflösung zu `ResolvedPolicy`
- Erzeugung der `BuildingOrder`
- Übergabe an den Foreman

Nicht verantwortlich für Bauwissen oder Topologie.

---

### SiteManager / Foreman

Domain-Orchestrator.

Verantwortlich für:

- Plugin-Bootstrap
- Dispatch der Spezialisten über Plugin-Registry
- Konfliktauflösung zwischen Spezialisten
- `FramePlan` und `RoofPlan` als koordinierte Outputs

Nicht verantwortlich für Topologie, Member-Erzeugung oder Physikprüfung.

---

### Topology Planner

Type-Plugin.

Verantwortlich für:

- archetypspezifische Policy-Auflösung
- `SemanticPlan` (inkl. `OpeningsPlan`)

---

### Joiner

Type-Plugin.

Verantwortlich für:

- `InteriorPlan`
- Raumlogik, Zonen, Erschließung

---

### Frame Producer

Domain-Rolle.

Verantwortlich für:

- Ableitung von `FramePlan` aus `SemanticPlan`
- konstruktive Umsetzung des `OpeningsPlan`

---

### Roof Producer

Domain-Rolle.

Verantwortlich für:

- Ableitung von `RoofPlan` aus `FramePlan` und Policy

---

### Renderer

Blender-Rolle.

Verantwortlich für:

- Emission von Geometrie aus Artefakten

---

## Registrierungsprinzip

Archetypen registrieren sich selbst.

Core enthält keine Liste konkreter Archetypen.

Type-Plugins registrieren:

- `archetype_id`
- `topology_planner`
- `construction_grammar`

Domain-Plugins registrieren:

- `construction_grammar`
- `foreman`

---

## Verbindliche Regeln

### Regel 1

Core darf keine konkreten Archetypen kennen.

### Regel 2

Types dürfen keine strukturellen Members erzeugen.

### Regel 3

Domains sind allein verantwortlich für `FramePlan` und `RoofPlan`.

### Regel 4

Renderer dürfen keine Struktur ableiten.

### Regel 5

Artefakte sind die einzige Wahrheit zwischen den Layern.

### Regel 6

Neue Baugrammatiken dürfen den Core nicht ändern müssen.

---

## Pipeline

Die kanonische BVILLAGE-Pipeline lautet:

```text
Context
→ Commissioner
→ BuildingOrder (mit ResolvedPolicy)
→ Foreman
→ Topology Planner
→ SemanticPlan (inkl. OpeningsPlan)
→ Frame Producer
→ FramePlan
→ Roof Producer
→ RoofPlan
→ Joiner
→ InteriorPlan
→ Inspector
→ Appraiser
→ Renderer
→ Blender Objects
```
