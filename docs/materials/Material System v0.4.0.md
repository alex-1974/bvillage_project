BVILLAGE
Material System Specification
Version: v0.4.0
Status: MVP – Structural Intelligence

---

# 1. Designprinzip

Material ist im System **nicht gleich Optik** und **nicht gleich Geometrie**.

Das System trennt strikt:

1. **MaterialBase** → physikalische Wahrheit (PPV-relevant)
2. **MaterialVariant** → konkrete Bauvariante (Handels-/Artenebene)
3. **Condition / Finish** → visuelle & oberflächliche Modifikatoren
4. **ProductForm** → Geometrieebene (kein Material)

Diese Trennung ist dauerhaft gültig.

---

# 2. Ebene A – MaterialBase (zeitlos, klein, stabil)

## Definition

MaterialBase beschreibt das physikalische Verhalten eines Werkstofftyps.

Es ist:

* historisch neutral
* regionenunabhängig
* minimal in Anzahl
* PPV-relevant

## MVP MaterialBase-Liste

### Timber

* `timber.hardwood`
* `timber.softwood`

### Masonry

* `masonry.brick`
* `masonry.stone_sandstone`
* `masonry.stone_granite`

### Binder

* `binder.mortar_lime`
* `binder.mortar_hydraulic`
* `binder.concrete`

### Other

* `glass.soda_lime`
* `metal.wrought_iron`

→ Gesamt: ca. 10–12 Basen.
Diese Zahl bleibt klein.

## Physikalische Parameter (MVP)

Minimal erforderlich:

* density_kg_m3
* E_modulus_GPa
* bending_strength_MPa
* compression_strength_MPa (optional)
* shear_strength_MPa (optional)

PPV arbeitet ausschließlich mit diesen Werten.

---

# 3. Ebene B – MaterialVariant (kontrolliert wachsend)

## Definition

MaterialVariant repräsentiert konkrete Arten oder Qualitätsklassen.

Eine Variant verweist immer auf genau eine MaterialBase.

### Beispiel: Holz

* `timber.oak`        → base = timber.hardwood
* `timber.beech`      → base = timber.hardwood
* `timber.spruce`     → base = timber.softwood
* `timber.pine`       → base = timber.softwood
* `timber.larch`      → base = timber.softwood

### Beispiel: Stein

* `stone.sandstone_weak`
* `stone.sandstone_strong`
* `stone.granite`

### Beispiel: Ziegel

* `brick.historic_low`
* `brick.historic_mid`
* `brick.historic_high`

Variant darf:

* physikalische Werte leicht überschreiben (z.B. oak vs spruce)
* eigenes RenderProfile haben

Variant darf nicht:

* neue physikalische Kategorie einführen

---

# 4. Ebene C – Condition / Finish (keine neue Material-ID!)

## Definition

Condition und Finish sind **Modifier**, keine Materialien.

Sie ändern:

* Rendering
* ggf. leichte mechanische Faktoren (später)

Sie ändern nicht:

* MaterialBase
* strukturelle Identität

## Condition (Alter/Zustand)

* `fresh`
* `weathered`
* `aged`

Optional später:

* `rotting`
* `damaged`

MVP: nur visuelle Wirkung.

## Finish (Oberfläche)

* `sawn`
* `planed`
* `oiled`
* `painted`
* `whitewashed`
* `tarred`

Finish beeinflusst:

* Roughness
* Farbe
* Normal/Detail
* Patina

Nicht: E-Modul oder Festigkeit (MVP).

---

# 5. Ebene D – ProductForm (GEOMETRIE, nicht Material)

Holz als Stamm, Brett, Balken ist kein Materialproblem.

Es ist ein geometrisches / strukturelles Thema.

Beispiele:

* `product_form = "log"`
* `product_form = "beam"`
* `product_form = "plank"`
* `section_profile = "rect_140x140"`

Diese Information gehört in:

* Member
* FramePlan
* Builder

Nicht in MaterialRegistry.

---

# 6. Material-ID-System (kanonisch)

## Format

```
<family>.<variant>
```

Beispiele:

* `timber.oak`
* `brick.historic_mid`
* `stone.granite`
* `binder.mortar_lime`

Condition und Finish werden nicht in die ID kodiert.

Sie sind separate Attribute.

---

# 7. Determinismus

Materialauflösung muss deterministisch sein.

```
resolve_material(member, ctx)
```

Variation erfolgt ausschließlich über:

```
sample_render(material, seed, salt)
```

salt = stabiler Member-Identifier

Kein globaler RNG.

---

# 8. MVP-Grenzen (v0.4.0)

Wir gehen bewusst nicht in:

* Holzfeuchteklassen
* Sortierklassen
* Astigkeit
* Faserverlauf
* DIN- oder Eurocode-Klassen
* Mikrorissmodellierung
* chemische Alterung

Diese gehören in spätere Structural-Phasen.

---

# 9. Entscheidung: Wie weit gehen wir?

Für v0.4.0 gilt:

* 10–15 MaterialBase maximal
* 20–30 MaterialVariant maximal
* Condition rein visuell
* ProductForm strikt getrennt
* PPV nutzt nur Base/Variant-Werte

Damit ist das System:

* skalierbar
* sauber getrennt
* policy-erweiterbar
* rendering-kompatibel
* structural-intelligence-fähig

---

Wenn du willst, gehen wir als nächstes in:

A) konkrete Python-Datamodelle
oder
B) Registry-Implementierungsarchitektur
oder
C) Policy-Integration (wer darf welches Material wann nutzen?)

