# RES_GRUNDUNG_SCHWELLE
## Gründung und Schwelle im Fachwerkbau: Regionale und epochale Differenzierung

---

```yaml
tier: 2
authority: SCOPE
status: Offen — Inhalt ausstehend
version: 0.1
datum: 2026-03-07
bereich: FACHWERK/KONSTRUKTION
references:
  - RES_KONSTRUKTION_ALLGEMEIN.md
  - RES_BAUPRAXIS_QUANTITATIV.md
  - RES_FACHWERK_HISTORISCH.md
```

---

## Zweck dieses Dokuments

Die Trennung des Ständers vom Erdboden — Pfosten nicht mehr eingraben,
stattdessen auf Stein oder Schwelle stellen — ist der konstruktive
Ursprungsakt des Fachwerkbaus (siehe `RES_FACHWERK_HISTORISCH.md` §1.1).

Gründung und Schwelle sind deshalb nicht nur technische Details, sondern
domain-definierende Parameter. Ihre regionale und epochale Differenzierung
bestimmt:
- ob `domain = fachwerk` überhaupt vorliegt
- welche Steinarten und Mörtel für `ConstraintsPolicy` verfügbar sind
- welche Feuchtelasten auf die Schwelle wirken

Offenes Forschungsfeld aus vorgelagerten Dokumenten: KON-004.

---

## Was bereits bekannt ist

### Fundamenttiefen Profanbau (aus RES_BAUPRAXIS_QUANTITATIV.md §4.9, [MITTEL])

| Wandtyp | Dicke / Tiefe |
|---|---|
| Fundament (Profanbau) | 70–90 cm breit, 60–100 cm tief |
| Stadthaus mit Gewölbekeller | Kellerwände 80–120 cm |

### Schwelle als Bauteil (aus RES_BAUPRAXIS_QUANTITATIV.md §4.1, [MITTEL])

- Breite = Wanddicke: typisch 16–22 cm breit, Höhe 14–20 cm
- Eiche bevorzugt (Kernholz, feuchteresistent)

### Pfostenbau als Vorläufer (aus RES_FACHWERK_HISTORISCH.md §1.1, [HART])

Der Übergang Pfostenbau → Ständer auf Schwelle ist der definierende
Moment. Dendrochronologisch datierbar auf die zweite Hälfte des
13. Jahrhunderts für Deutschland.

---

## Geplanter Inhalt

1. Gründungstypen nach Region und Epoche:
   - Trockensteinlager (früh, universell)
   - Mörtelmauerwerk-Fundament (ab 13. Jh. städtisch)
   - Gewölbekeller (städtisch, ab 13./14. Jh.)
   - Natursteinschwelle direkt auf Terrain (ländlich, spät)
2. Schwellenauflager: Steinlager, Ziegellager, Holzschwellenstein
3. Feuchtemanagement: Steinlager-Abstände, Belüftungsprinzipien,
   Eichenholz-Präferenz (Kernholz)
4. Regionale Verfügbarkeit von Steinarten → `ConstraintsPolicy`
5. Zusammenhang Gründungstiefe → Bodenfrost → Region
6. BVILLAGE-Parameter: `foundation_type`, `sill_material`,
   `sill_stone_bearing_type`

---

## Primärquellen (zu beschaffen)

- Klein, Ulrich: DGAMN-Mitteilungen Bd. 24, 2012.
  (Grabungsbefunde mit Fundamentspuren früher Fachwerkbauten)
- Freilichtmuseen: Aufmaßdaten zu Schwellendetails
- Landesdenkmalpflege: Restaurierungsberichte mit Fundamentbefunden

---

## BVILLAGE-Relevanz

`ConstraintsPolicy` muss Steinverfügbarkeit nach Region kodieren.
`MaterialRegistry` braucht Schwellen-Material-Klasse.
Ohne dieses Dokument: Gründung und Schwelle sind nicht validierbar;
`PhysicalPlausibilityValidator` kann keine Feuchtelasten prüfen.

---

*Status: SCOPE — Inhalt ausstehend. Primärquellen müssen ausgewertet werden.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
