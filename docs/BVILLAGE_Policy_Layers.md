# BVILLAGE Policy Layers

## Zweck

Dieses Dokument definiert die verbindliche Struktur der Policy-Schichten
in der BVILLAGE Engine.

Policies steuern Variation und historische Plausibilität, ohne die
Layer-Trennung der Engine zu verletzen.

Policies dürfen Parameter setzen und Präferenzen ausdrücken, aber keine
Geometrie erzeugen.

---

# Grundprinzip

Policies sind **deklarativ**.

Sie beschreiben:

- erlaubte Bereiche
- bevorzugte Werte
- historische oder regionale Variation

Policies dürfen **nicht**:

- Artefakte erzeugen
- Geometrie berechnen
- Renderer beeinflussen
- Layer-Verantwortlichkeiten überschreiben

Jede Policy ist ein **Delta** — ein Satz Overrides auf dem kanonischen
Parameter-Baum. Eine Policy, die nichts beiträgt, ist leer.
Eine leere Policy ändert nichts.

---

# Policy Layer

BVILLAGE verwendet zehn Policy-Schichten, die in definierter Reihenfolge
aufgelöst werden — von generisch nach spezifisch. Spätere Schichten
überschreiben frühere.

```text
1  BaseTypePolicy
→ 2  TopologyModifierPolicy
→ 3  VerticalPolicy
→ 4  RoofPolicy
→ 5  OpeningsPolicy
→ 6  FunctionPolicy
→ 7  StylePolicy
→ 8  CulturePolicy
→ 9  ConstraintsPolicy
→ 10 NoisePolicy
```

---

# Die zehn Schichten

## 1 BaseTypePolicy

**Scope:** Archetyp-Defaults

Definiert, was gilt, wenn kein weiterer Kontext bekannt ist.
Jeder Archetyp bringt seine eigene `BaseTypePolicy` mit.
Alle anderen Schichten sind Overrides darauf.

---

## 2 TopologyModifierPolicy

**Scope:** Grundriss-Modifikation

Optionale Grundrissmodifikationen: L-Form, T-Form, U-Form.
Verändert die räumliche Geometrie des Archetyps, ohne den Archetyp
selbst zu ersetzen.

---

## 3 VerticalPolicy

**Scope:** Vertikale Ausdehnung

Geschosszahl, Dachgeschossnutzung, Vorkragungen (Jettying).

---

## 4 RoofPolicy

**Scope:** Dachform

Dachtyp, Neigungsbereiche, Traufhöhe.

---

## 5 OpeningsPolicy

**Scope:** Öffnungsprogramm

Öffnungsbedarf, Licht- und Privatheitspräferenzen.

---

## 6 FunctionPolicy

**Scope:** Nutzungstyp und soziale Funktion

Gebäudenutzung und wirtschaftliche Funktion: Wohnen, Landwirtschaft,
Lagerung, Civic, Sakral. Steuert Zonenprogramm, Öffnungscharakter,
Repräsentationsrichtung, Tiernutzungsintegration.

`FunctionPolicy` ist ein **Pflichtfeld** in jeder `BuildingOrder`.
Default: `building_use=RESIDENTIAL`.

Positioniert zwischen `OpeningsPolicy` und `StylePolicy` —
Nutzungsunterschiede sind weder Archetyp- noch Stilfragen.

---

## 7 StylePolicy

**Scope:** Region × Epoche × Wohlstand × Siedlungstyp

Die breiteste Modulationsschicht. Berührt nahezu jeden Parameterbereich,
operiert aber ausschließlich innerhalb der von Domain und Archetyp
gesetzten Grenzen.

`StylePolicy` darf **nicht**:
- die Construction Domain wechseln
- den Archetyp ersetzen
- funktionale Unterschiede codieren (→ `FunctionPolicy`)

Wenn eine regionale Variation eine andere Strukturgrammatik erfordert,
ist das eine neue Domain oder ein neuer `CulturePolicy`-Branch —
kein `StylePolicy`-Variant.

---

## 8 CulturePolicy

**Scope:** Domain-spezifische Konstruktionskultur

Tacit knowledge der Baupraxis einer gegebenen Tradition:
typischer Member-Abstand, bevorzugte Aussteifungsmuster, Infill-Logik,
Redundanzpräferenzen, wie nah an physikalischen Grenzen gebaut wurde,
welche Spannweiten als normal oder übermäßig galten.

`CulturePolicy` verändert **nicht** die Physik. Sie moduliert, wie die
Domain ihre Strukturgrammatik innerhalb physikalisch erlaubter Grenzen
ausübt.

`CulturePolicy` und Domain lesen Region und Epoche nicht direkt.
Sie konsumieren bereits aufgelöste Policy-Daten — was
„Norddeutschland, 16. Jahrhundert" bedeutet, hat `StylePolicy`
bereits verarbeitet.

---

## 9 ConstraintsPolicy

**Scope:** Harte und weiche Constraints

Harte Constraints blockieren die Generierung.
Weiche Constraints erzeugen einen gewichteten Penalty, den der
Appraiser bei der Kandidatenauswahl berücksichtigt.

---

## 10 NoisePolicy

**Scope:** Deterministische Mikrovariation

Kontrollierte Variation innerhalb erlaubter Parameterbänder.
Einziger Zweck: visuell identische Gebäude innerhalb einer Siedlung
verhindern. Erzeugt keine strukturelle Variation.

---

# Auflösungsregel

```
resolve_policy_stack(ctx) → ResolvedPolicy
```

Einziger Einstiegspunkt. `ResolvedPolicy` muss Invarianten-Validierung
bestehen, bevor die Planung beginnt.

Unbekannte Patch-Keys erzeugen einen HARD Issue.
Stilles Fallback-Verhalten ist verboten.

---

# Expansionsregel

Neue Achsen treten als optionale Patch-Slots ein. Der Default ist
neutral — kein Effekt. Bestehende Archetypen und Domains erfordern
keine Modifikation, wenn eine neue Achse hinzugefügt wird.

Wenn das Hinzufügen einer neuen Achse Änderungen an bestehendem Code
erfordert, ist das ein Designfehler — kein Feature.

---

# Klassifikationshilfe

| Frage | Schicht |
|---|---|
| Andere Lastpfade oder Member? | Neue `construction_grammar` / Domain |
| Andere Zonanordnung oder Raumhierarchie? | Neuer Archetyp oder `TopologyModifierPolicy` |
| Andere Nutzung bei gleicher Topologie? | `FunctionPolicy` |
| Anderer Dachtyp, Geschosszahl? | `RoofPolicy` / `VerticalPolicy` |
| Andere Region, Epoche, Wohlstand? | `StylePolicy` |
| Oberflächliche Diversität innerhalb identischer Parameter? | `NoisePolicy` |

Im Zweifel: auf der höheren Schicht klassifizieren. Eine Promotion von
Style zu Domain ist eine saubere Entscheidung. Eine spätere Demotierung
verursacht Rewrites.
