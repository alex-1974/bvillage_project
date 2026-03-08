# RES_OEFFNUNGEN_INNENRAUM
## Öffnungsgrammatik und Innenraumorganisation im Fachwerkbau

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
  - RES_ARCHETYPE_HALLENHAUS.md
  - RES_BAUPRAXIS_QUANTITATIV.md
```

---

## Zweck dieses Dokuments

Öffnungen (Fenster, Türen, Tore) sind konstruktive Eingriffe in das
Ständer-Riegel-Raster, nicht dekorative Elemente. Jede Öffnung erfordert
Torpfosten (jamb posts), Sturz (lintel) und Anpassung der Aussteifung
(Bracing darf Öffnungen nicht schneiden).

Die Innenraumorganisation folgt der Tragwerkslogik: Räume sind Zonen
um Ständerachsen, nicht modern freie Grundrisse. Dieses Dokument soll
die vollständige Öffnungsgrammatik und Raumzonenlogik nach Archetyp,
Epoche und Region liefern.

Offenes Forschungsfeld aus vorgelagerten Dokumenten: KON-003.

---

## Was bereits bekannt ist

### Öffnungsmaße (aus RES_ARCHETYPE_HALLENHAUS.md §4.4, [MITTEL])

| Parameter | Normalbereich |
|---|---|
| `door_width_m` | 0,8–1,2 m |
| `gate_width_m` | 2,0–3,5 m |
| `window_sill_z_m` | 0,7–1,0 m |
| `lintel_z_m` | 1,8–2,2 m |

### Konstruktionspflichten bei Öffnungen (aus RES_ARCHETYPE_HALLENHAUS.md §9)

- Keine Öffnung ohne `jamb + lintel + Anschlüsse`
- Bracing darf Öffnungen nicht schneiden
- Tore erfordern zusätzliche Aussteifung

### Raumzonen Hallenhaus (aus RES_ARCHETYPE_HALLENHAUS.md §10)

Diele / Stallzone / Hochlager / Wohnzone (Flett) / Kammern.
Abgrenzung primär durch Ständerreihen, sekundär durch leichte Innenwände.

---

## Geplanter Inhalt

1. Öffnungsgrammatik nach Archetyp:
   - Hallenhaus: Giebeltor als primäre Öffnung; Fenster klein und hoch
   - Stadthaus: Schauseite zur Straße; Ladenöffnung EG; Fensterachsen OG
   - Ernhaus: Traufseiten-Eingang; Fenster symmetrisch zur Mittelachse
2. Fenster- und Türproportionen nach `epoch_band`:
   - Frühmittelalter: sehr kleine, hochgesetzte Öffnungen
   - Spätmittelalter: wachsende Fenster, Maßwerk-Einfluss
   - Renaissance/Barock: rhythmisierte Fensterachsen, Doppelständer
3. Sturzkonstruktionen: einfacher Sturz, Entlastungsbogen, Schichtenfolge
4. Innenraumorganisation nach Archetyp-Familie:
   - Hallenbau: Zonierung um Ständerachsen
   - Stadthaus: Vertikale Schichtung (EG Gewerbe, OG Wohnen, DG Lager)
   - Ernhaus: Querflur (Ern) als Erschließungsachse
5. `OpeningsPolicy`-Parameter vollständig definieren

---

## Primärquellen (zu beschaffen)

- Stiewe, Heinrich: Fachwerkhäuser in Deutschland. 2007.
  (Grundformen, Öffnungen, Innenausbau)
- Bedal, Konrad: Historische Hausforschung in Franken.
  (Ernhaus-Varianten, Öffnungsgrammatik)
- Freilichtmuseum Hessenpark / Bad Windsheim:
  (Aufmaßdaten zu Archetypen)

---

## BVILLAGE-Relevanz

`OpeningsPolicy` und `InteriorPlanner` sind abhängig von diesem Dokument.
Ohne vollständige Öffnungsgrammatik: keine historisch plausiblen
Fenster- und Torproportionen; Raumzonenlogik nur für Hallenhaus belegt.

---

*Status: SCOPE — Inhalt ausstehend. Primärquellen müssen ausgewertet werden.*
*© 2026 Alexander Bernardi — CC-BY-SA 4.0*
