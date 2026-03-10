# RES_VERBINDUNGSTECHNIK
## Verbindungstechnik im Fachwerkbau: Datierte Sequenz und konstruktive Klassifikation

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
  - RES_BAUGRAMMATIKEN.md
```

---

## Zweck dieses Dokuments

Verbindungstypen bestimmen Kraftübertragungskapazitäten und damit die
Dimensionierungslogik der `ConstructionCulturePolicy`. Insbesondere:

- `max_utilization_ratio` hängt vom Verbindungstyp ab
- V-BLATT: niedrigere Kapazität → höherer `overdimension_factor`
- V-ZAPF: höhere Kapazität → niedrigerer `overdimension_factor`
- Der Übergang V-BLATT → V-ZAPF ist ein `epoch_band`-Signal

Hewett (Structural Carpentry in Medieval Essex) hat für England gezeigt,
dass Verbindungstypen einer historischen Sequenz folgen und datierbar sind
wie Keramik. Eine analoge datierte Sequenz für den deutschsprachigen Raum
fehlt in der Forschungsliteratur — das ist die explizite Lücke
dieses Dokuments.

Offene Forschungsfelder aus vorgelagerten Dokumenten: KON-001, QNT-004.

---

## Was bereits bekannt ist (aus RES_KONSTRUKTION_ALLGEMEIN.md §3)

| ID | Name | Belastbarkeit | Epoche |
|---|---|---|---|
| V-BLATT | Verblattung | Scherbeanspruchung; begrenzte Zugkraft | früh, bis 15. Jh.; alemannisch |
| V-ZAPF | Verzapfung | Druck gut, Zug begrenzt | ab 13. Jh.; ab 16. Jh. dominant |
| V-KAMM | Verkämmung | Druckkraft; keine Zugkraft | Schwellenkreuzung |
| V-DURCHSCH | Durchschossen | Hohe Schubkraft; Ständer geschwächt | Ständerbau; bis 16. Jh. |
| V-STURZ | Sturzriegel | Biegung auf Riegel | universal |

Epochensignal: Die konstruktiven Entwicklungen des Fachwerkbaus,
einschließlich des Übergangs V-BLATT → V-ZAPF, waren 1600 abgeschlossen.
**[HART]**

---

## Geplanter Inhalt

1. Datierte Sequenz der Verbindungstypen für den deutschsprachigen Raum
   (Primärliteratur: Eißing, Klein, Gerner)
2. Verbindungstyp nach Bauteil-Kombination (Ständer↔Rähm, Balken↔Ständer,
   Pfette↔Binder, Strebe↔Ständer)
3. Zapfengeometrie: Länge, Breite, Tiefe nach Epoche und Belastungsart
4. Holznagel-Parameter: Durchmesser, Länge, Anzahl pro Verbindung
5. Regionale Differenzierung: alemannisch (V-BLATT länger erhalten) vs.
   fränkisch/norddeutsch (V-ZAPF früher dominant)
6. BVILLAGE-Implikationen: `JoineryHint`/`ConnectionSpec` im FramePlan;
   Validierungsregeln im `PhysicalPlausibilityValidator`

---

## Primärquellen (zu beschaffen)

- Hewett, C. A.: English Historic Carpentry. Linden Publishing, 1980.
  (Methodisches Vorbild für datierte Sequenz)
- Eißing, Thomas et al.: Vorindustrieller Holzbau. Heidelberg 2023.
  (Terminologie und Systematik, enthält Verbindungstypen)
- Gerner, Manfred: Fachwerk. DVA, München 2007.
  (Verbindungsdetails mit historischen Zeichnungen)
- Klein, Ulrich: DGAMN-Mitteilungen Bd. 24, 2012.
  (Epochenübergänge, enthält implizite Verbindungssequenz)

---

## BVILLAGE-Relevanz

Der `PhysicalPlausibilityValidator` kann Verbindungsplausibilität nur
prüfen, wenn Verbindungstypen und ihre Kapazitäten im System kodiert sind.
Ohne dieses Dokument: keine Zapfenvalidierung, kein Verbindungs-Epochensignal.

Zieldatenstruktur (vorläufig):
```python
@dataclass(slots=True)
class ConnectionSpec:
    joint_type: str          # "blatt" | "zapfen" | "kamm" | "durchschossen"
    tenon_length_mm: float   # Zapfenlänge
    tenon_width_ratio: float # Breite als Anteil Holzquerschnitt (ca. 1/3)
    peg_count: int           # Holznagel-Anzahl
    peg_diameter_mm: float
    epoch_range: tuple[int, int]
    capacity_factor: float   # relativ zu V-ZAPF Standard = 1.0
```

---

*Status: SCOPE — Inhalt ausstehend. Primärquellen müssen ausgewertet werden.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
