# RES_ARCHETYPE_SONDERFAELLE
## Sonder- und Grenzfälle der Hallenbau- und Hybridarchitektur

---

```yaml
tier: 2
authority: SCOPE
status: Offen — Inhalt ausstehend
version: 0.1
datum: 2026-03-07
bereich: FACHWERK/ARCHETYPEN
references:
  - RES_BAUGRAMMATIKEN.md
  - RES_ARCHETYPE_HALLENHAUS.md
  - RES_FACHWERK_HISTORISCH.md
  - RES_KONSTRUKTION_ALLGEMEIN.md
```

---

## Zweck dieses Dokuments

Dieses Dokument sammelt Archetypen und Grenzfälle, für die entweder:

1. Die Klassifikation noch nicht entschieden ist
   (`archetype` vs. `policy_variant`), oder
2. Primärquellen für die Konstruktionslogik fehlen, oder
3. Eine `hybrid_strategy` konzeptionell noch nicht definiert ist

Alle offenen Forschungsfelder, die auf dieses Dokument verweisen:
GRM-001, GRM-002, GRM-003, GRM-004, GRM-005, GRM-007,
HAL-004, HAL-005, HIS-001, HIS-002, DEF-001.

---

## 1. Gulfhaus (FW-GULF)

### Bekannt

Wo: Nordseeküste, Friesland bis Schleswig-Holstein.
Wann: 16.–19. Jahrhundert.

Der **Gulf** ist der zentrale Großraum — allseitig umschlossener
Ernteraum von bis zu 12 m Höhe. Konstruktion: enge Ständerpaarfolge
(Vierkante), die einen Tunnel aus Holz bilden. Weit heruntergezogenes
Reetdach. **[MITTEL]**

Kanonisches Beispiel: Ostfriesisches Landesmuseum Aurich; Freilichtmuseum Leer.

### Offene Fragen (GRM-001, HAL-004, HIS-001)

- Ist FW-GULF ein eigenständiger `archetype` oder ein `policy_variant`
  von `FW-LH-ND`?
- Spannweiten und Stützenlogik weichen erheblich ab — das spricht für
  eigenständigen Archetyp.
- Primärquellen zu Vierkant-Konstruktionslogik, Firsthöhe und
  Bindergeometrie fehlen.

### Benötigte Primärquellen

- IG Baupflege Nordfriesland
- Ostfriesisches Landesmuseum Aurich (Aufmaßdaten)
- Bedal, Konrad: Hallenhäuser in Deutschland

---

## 2. Haubarg (FW-HAUB)

### Bekannt

Wo: Nordfriesland, Eiderstedt.
Wann: 17.–19. Jahrhundert.

Annähernd quadratischer Grundriss, allseitig abgewalmtes Reetdach.
Innen: ein einziger Vierkant — zentraler Stapelraum von 10–17 m Höhe.
Konstruktionsholz importiert aus Pommern, Polen, Norwegen, Schweden.
Steckverbindungen, nicht geleimt — Gebäude abbaubar. **[MITTEL]**

Kanonisches Beispiel: Haubarg Witzwort, Eiderstedt.

### Offene Fragen (HAL-005, HIS-001)

- Konstruktionslogik des Vierkants: wie ist der zentrale Hochraum
  statisch gelöst?
- Verhältnis zur Hallenhaus-Logik: kein Innenständergerüst im Sinne
  von FW-LH-ND, sondern Umfassungsrahmen?
- Klassifikation: eigenständiger `archetype` oder extreme
  `policy_variant` von FW-GULF?

### Benötigte Primärquellen

- IG Baupflege Nordfriesland
- Freilichtmuseum Schleswig-Holstein

---

## 3. Umgebindehaus (FW-UMG)

### Bekannt

Wo: Oberlausitz, Nordböhmen, Niederschlesien.
Wann: 15.–19. Jahrhundert.

Zwei simultane Tragsysteme in einem Gebäude: **Blockstube** (Blockbau-Domain;
trägt sich selbst) + **Umgebinderahmen** (Fachwerk-Domain; trägt Dach
unabhängig). Stube kann schrumpfen ohne Rahmen zu belasten. **[HART]**

Kanonisches Beispiel: Umgebindehausmuseum Markersdorf; Ebersbach/Sachsen.

### Offene Fragen (GRM-002, DEF-001)

- `hybrid_strategy` für FW-UMG ist konzeptionell nicht definiert.
- Zwei parallele `FramePlan`-Logiken (Blockbau-Stube + Fachwerk-Rahmen)
  müssen unabhängig existieren und interagieren.
- Schnittstelle zwischen Blockbau-Domain und Fachwerk-Domain:
  wie wird der Lastpfad-Wechsel im System abgebildet?

### Benötigte Primärquellen

- Informationszentrum Umgebindehaus, Hochschule Zittau/Görlitz
- Freilichtmuseum Markersdorf

---

## 4. Niederlande / Flandern (FW-NL, FW-FL)

### Bekannt

Holz-Stadtarchitektur in Limburg (NL) und Lüttich (B). Erdgeschosse
häufig in Stein, Obergeschosse Fachwerk. Schlichtere Fassaden als
deutsches Fachwerk. **[MITTEL]**

### Offene Fragen (GRM-005, HIS-002)

Keine Primärquellen zu Dutch timber townhouse oder Flemish guild house
verfügbar. Das ist eine explizite Forschungslücke.

Benötigte Klärungen:
- Konstruktive Eigenständigkeit oder Variante der norddeutschen Grammatik?
- `archetype_id` für BVILLAGE-Taxonomie
- Epochenband und regionale Abgrenzung

### Benötigte Primärquellen

- Monumentenzorg Nederland (Rijksdienst voor het Cultureel Erfgoed)
- Openluchtmuseum Arnhem (Niederländisches Freilichtmuseum)
- Vlaamse Overheid: Onroerend Erfgoed

---

## 5. Stabbau (FW-STV)

### Bekannt

Historische Bauweise mit Kernpfosten in Nut-Schlitz-Konstruktion,
bekannt vor allem aus norwegischen Stabkirchen. In Deutschland ab ca.
12./13. Jahrhundert durch Ständerbau abgelöst. Nur SCHWACH-Evidenz
für Profanbauten. **[SCHWACH]**

### Offene Fragen (GRM-003)

- Konstruktionslogik (Kernpfosten) weicht von BOX_FRAME ab.
- Ist FW-STV eine eigenständige `ConstructionDomain` oder ein
  Sonderfall von `fachwerk.standerbau`?
- Für Deutschland: Profanbauten in Stabbauweise — Primärliteratur fehlt.

### Benötigte Primärquellen

- Ahrens, Claus: Die frühe Holzbaukunst in Mitteleuropa.
- Untersuchungen Stabbau (deutsch) — noch nicht identifiziert.

---

## 6. Aisled Frame vs. Zweiständerhaus (ENG-AISL vs. FW-LH-2S)

### Offene Frage (GRM-007)

Konzeptionelle Grenze zwischen deutschen Varianten (FW-LH-2S:
Zweiständerhaus als Hallenhaus-Variante) und englischen Aisled Halls
(ENG-AISL: eigenständige Grammatik aus Cruck/Box-Frame-Tradition) ist
nicht vollständig belegt.

Konkrete Frage: Ab wann ist eine konstruktive Ähnlichkeit ausreichend
für denselben Archetyp, und ab wann erzwingt die Grammatik-Verschiedenheit
getrennte Archetypen?

Bezugsdokument: `RES_BAUGRAMMATIKEN.md` §5 (Wealden-Korrektur als
Beispiel für gelöste Klassifikationsfrage).

---

## 7. Geesthardenhaus (GH-GEEST)

### Bekannt

Wo: Schleswig, Jütland. Wann: 17.–19. Jahrhundert.
Außenwände tragend, keine Innenständer, quergeteilte Räume.
Traufständig, moderate Spannweite.

Kanonische Bestände: Freilichtmuseum Molfsee Kiel; Borsbüll Nordfriesland.

### Status

Vorerst als eigenständiger `archetype` gelistet (ARCH_TAXONOMY.md).
Konstruktionslogik ist näher an Ernhaus-Familie als an Hallenbau-Familie.
Vollständige Dokumentation: in diesem Dokument ausstehend.

---

## Priorisierung

| Archetyp | Priorität | Begründung |
|---|---|---|
| FW-GULF | Hoch | Häufig; Klassifikationsfrage blockiert Roadmap |
| FW-UMG | Hoch | `hybrid_strategy` blockiert Domain-Definition |
| FW-HAUB | Mittel | Weniger häufig; Primärquellen schwer zugänglich |
| FW-NL / FW-FL | Niedrig | Phase 2; pan-europäische Erweiterung |
| FW-STV | Niedrig | Nur SCHWACH-Evidenz; Profanbau-Relevanz unklar |
| ENG-AISL vs. FW-LH-2S | Mittel | Konzeptuelle Klärung; keine Primärquellen nötig |

---

*Status: SCOPE — Inhalt ausstehend. Priorisierung gilt für nächste Forschungsphase.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
