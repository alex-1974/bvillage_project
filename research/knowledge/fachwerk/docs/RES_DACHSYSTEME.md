# RES_DACHSYSTEME
## Dachsysteme im Fachwerkbau: Konstruktionslogik, Neigungswinkel, regionale Dominanzen

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
  - RES_ARCHETYPE_HALLENHAUS.md
```

---

## Zweck dieses Dokuments

Für BVILLAGE ist das Dachsystem kein Blender-Parameter, sondern ein
Grammar-Parameter, der Statik und FramePlan bestimmt (siehe
`RES_ARCHETYPE_HALLENHAUS.md` §5). Dieses Dokument soll die vollständige
Klassifikation der historischen Dachsysteme, ihre konstruktive Logik
und ihre regionalen und epochalen Dominanzen liefern.

Offene Forschungsfelder aus vorgelagerten Dokumenten: KON-002, QNT-005, HAL-002.

---

## Was bereits bekannt ist

### Dachsysteme (aus RES_ARCHETYPE_HALLENHAUS.md §5)

| System | Prinzip | Typische Spannweite | Regionale Tendenz |
|---|---|---|---|
| Sparrendach (rafter_pairs) | Sparrenpaare → Querrahmen / Rähm | bis 8 m | Universell, früh |
| Kehlbalkendach (collar) | Kehlbalken reduziert Sparrenspreizung | 6–12 m | Norddeutsch |
| Pfettendach (purlin) | Pfetten längs; Innenständer als Auflager | 8–18 m | Norddeutsch, Hallenhaus |
| Mischsysteme (mixed) | Kombinationen der o. g. | Variabel | Regional |

### Dachlasten (aus RES_BAUPRAXIS_QUANTITATIV.md §4.7, [HART])

| Material | kg/m² | Mindestneigung |
|---|---|---|
| Stroh / Reet (frisch) | 35–45 kg/m² | 45–60° |
| Holzschindeln | 15–25 kg/m² | 30–50° |
| Biberschwanz-Ziegel | 40–55 kg/m² | 35–60° |
| Mönch-Nonne | 50–70 kg/m² | 25–40° |
| Naturschiefer | 30–40 kg/m² | 25–45° |
| Sandsteinplatten | 60–90 kg/m² | 30–50° |
| Cotswold Kalkstein | 100+ kg/m² | 45–55° |

Schneelast Mitteleuropa: 0,5–2,0 kN/m², Berglagen höher.

---

## Geplanter Inhalt

1. Vollständige Dachsystem-Taxonomie: Sparrendach, Kehlbalkendach,
   Pfettendach, Hängewerk, Spannwerk, Hammerbalken (Westminster Hall)
2. Konstruktive Logik je System: Kraftpfad, member-Rollen, Auflagerpunkte
3. Regionale Dominanzen nach `region × epoch_band`:
   - Reet/Stroh: Norddeutsche Tiefebene, steile Neigung
   - Schindel: Alpenraum, mittlere Neigung
   - Ziegel: städtisch, ab 15./16. Jh.
   - Sandstein/Schiefer: Mittelgebirge
4. Neigungswinkel-Verteilungen (nicht nur Ranges, sondern Häufungen)
   aus Bauaufnahme-Korpora
5. Zusammenhang Dachdeckung → Dachneigung → Sparrenquerschnitt →
   `CulturePolicy.roof_pitch`
6. Mischsysteme: wann historisch plausibel

---

## Primärquellen (zu beschaffen)

- Eißing et al.: Vorindustrieller Holzbau. Heidelberg 2023.
  (Dachstuhltypen, regionale Verbreitung)
- Gerner, Manfred: Fachwerk. DVA, München 2007.
  (Dachkonstruktionen mit historischen Querschnitten)
- Bedal, Konrad: Historische Hausforschung.
  (Dachstuhlstudien norddeutscher Hallenhäuser)
- VAG-Dendrodaten (county-weise): implizite Dachsystem-Information
  aus Datierungen

---

## BVILLAGE-Relevanz

`RoofPolicy` erhält `roof_system` und `roof_pitch` als Output.
Diese Parameter beeinflussen:
- Sparrenquerschnitt und -abstand
- Pfettenlauf und Auflager
- Dachlast-Annahmen im `PhysicalPlausibilityValidator`
- Kompatibilität mit Dachdeckungs-Material (aus MaterialRegistry)

Ohne dieses Dokument: `RoofPolicy` muss mit Fallback-Werten arbeiten,
die nicht regionalisiert sind.

---

*Status: SCOPE — Inhalt ausstehend. Primärquellen müssen ausgewertet werden.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
