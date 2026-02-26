# Python Performance & Scalability – General Best Practices (BVILLAGE Scan)

Eine allgemeine Sammlung performanter, wartbarer und skalierbarer Coding-Praktiken für unser Projekt.

---

## 1. Streaming statt Materialisieren

### Ziel

Weniger Speicher, weniger Zwischenobjekte, frühere Abbrüche.

### Mittel

* Generatoren (`yield`)
* Generator-Expressions (`(f(x) for x in xs)`)
* `any()`, `all()`, `next(..., None)` für Early Exit
* `itertools` (`chain`, `islice`, `groupby`, `pairwise`)

### Beispiel

```python
if any(collides(m) for m in members):
    return False
```

---

## 2. Sort Once → Linear Merge

### Ziel

Komplexität reduzieren (O(n log n) + O(n) statt O(n²)).

### Mittel

* Werte sammeln
* Einmal sortieren
* In einem Durchlauf mergen (EPS/merge_tol)

Typische Einsatzfelder:

* Achsen
* Z-Levels
* Öffnungsintervalle
* Toleranz-Merges

---

## 3. Intervalle normalisieren (Union bilden)

### Ziel

Konfliktprüfungen vereinfachen.

Statt:

* Für jedes Member gegen jede Öffnung prüfen

Besser:

* Öffnungen pro Wand unionisieren
* Danach nur noch gegen disjunkte Intervalle prüfen

---

## 4. Datenstrukturen mit geringem Overhead

* `@dataclass(frozen=True, slots=True)` für viele kleine Value-Objekte
* Kleine Records ggf. als `tuple` oder `NamedTuple`
* `set`/`dict` für Membership-Tests (O(1))
* Bei großen numerischen Mengen: ggf. `array` oder `numpy`

---

## 5. Hot Loop Optimierungen (nur wenn nötig)

### Lokalisieren von Lookups

```python
append = result.append
for x in xs:
    append(process(x))
```

* Attribute-/Dict-Lookups in inner loops vermeiden
* Module-Funktionen lokal binden (`math = math`)

→ 5–20% Speed in echten Hotspots

---

## 6. Batch statt viele kleine Schritte

### Prinzip

Compute → Validate → Emit

* Daten zuerst vollständig sammeln
* Danach in einem Schritt weiterverarbeiten
* Keine „Build while deciding“-Logik

---

## 7. Caching gezielt einsetzen

Nur für **pure Funktionen**.

Geeignet für:

* Normalisierte Achsen
* Merges
* Teure Ableitungen

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def normalized_axes(key):
    ...
```

Cache-Key muss alle relevanten Inputs enthalten (Policy, Seed, Dims).

---

## 8. Parallelisierung bewusst einsetzen

### CPU-bound

* `ProcessPoolExecutor`

### IO-bound

* Threads möglich

Nicht parallelisieren:

* Kleine Jobs mit hohem Overhead
* Nicht thread-safe APIs

---

## 9. Logging effizient halten

* Kein f-String in Debug-Logs:

```python
log.debug("value=%s", value)
```

* Reports erst am Ende formatieren
* Keine String-Konkatenation im Hot Loop

---

## 10. Exceptions nicht als Normalfall

* Keine Exceptions für normalen Kontrollfluss
* In Hot Loops lieber `if` + Sentinel-Werte

---

## 11. Determinismus als Skalierungshebel

* Stabile Iterationsreihenfolge
* Explizite Sortierung
* Saubere Seed-Verwaltung

Vorteile:

* Reproduzierbarkeit
* Snapshot-Tests möglich
* Debugging vereinfacht

---

## 12. Profiling & Regression-Schutz

* Phasen-Timer (`time.perf_counter`)
* `cProfile` für echte Hotspots
* Kleine feste Benchmark-Cases
* Snapshot-Tests für deterministische Reports

---

# Priorisierung (ROI)

## Hoher Impact

* Sort once → merge
* Interval-Union
* Streaming + Early Exit
* Pure Core + Caching
* Batch-Processing

## Mittlerer Impact

* Slots/Frozen Dataclasses
* Determinismus erzwingen
* Logging sauber strukturieren

## Micro (nur nach Profiling)

* Lokale Bindungen in Loops
* Kleine Lookup-Optimierungen
* itertools statt manueller Schleifen

---

# Leitprinzip

Erst algorithmisch optimieren.
Dann Datenstruktur optimieren.
Erst ganz zuletzt Micro-Optimierung.

