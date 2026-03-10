# MATERIAL HIERARCHY – NATURSTEIN
Systemneutral, hierarchisch strukturiert  
(Ebene: MaterialClass → MaterialGroup → MaterialType → Variant)

Ziel:
- Geologisch sauber
- Erweiterbar (Region / Epoche / Qualität)
- Physik- und Render-tauglich

---

# 1. MaterialClass: NATURAL_STONE

Naturbelassene Gesteine, nicht gebrannt, nicht künstlich hergestellt.

---

# 1.1 MaterialGroup: SEDIMENTARY

## 1.1.1 MaterialType: LIMESTONE

- jurassic_limestone
- muschelkalk
- cretaceous_limestone
- oolitic_limestone
- dolomitic_limestone
- chalk

Optional Variants:
- fine_grain
- medium_grain
- coarse_grain
- fossil_rich
- dense
- soft

---

## 1.1.2 MaterialType: SANDSTONE

- red_sandstone
- grey_sandstone
- buntsandstein
- arkose
- quartz_sandstone

Variants:
- fine_grain
- coarse_grain
- clay_rich
- quartz_rich

---

## 1.1.3 MaterialType: TUFF

- volcanic_tuff
- calcareous_tuff

Variants:
- light
- dense
- porous

---

## 1.1.4 MaterialType: TRAVERTINE

- roman_travertine
- alpine_travertine

Variants:
- porous
- dense
- banded

---

## 1.1.5 MaterialType: MARL

- calcareous_marl
- clay_marl

---

# 1.2 MaterialGroup: IGNEOUS

## 1.2.1 MaterialType: GRANITE

- light_granite
- dark_granite
- coarse_granite
- fine_granite

---

## 1.2.2 MaterialType: BASALT

- columnar_basalt
- compact_basalt

---

## 1.2.3 MaterialType: PORPHYRY

- red_porphyry
- green_porphyry

---

# 1.3 MaterialGroup: METAMORPHIC

## 1.3.1 MaterialType: SLATE

- roofing_slate
- structural_slate
- thin_slate
- thick_slate

---

## 1.3.2 MaterialType: MARBLE

- white_marble
- polychrome_marble
- carrara_marble

---

## 1.3.3 MaterialType: GNEISS

- banded_gneiss
- coarse_gneiss

---

# 1.4 MaterialGroup: SPECIAL_NATURAL

Nicht klassisch strukturiert, aber historisch relevant.

## 1.4.1 MaterialType: FIELDSTONE
- glacial_fieldstone
- river_fieldstone

## 1.4.2 MaterialType: PUMICE
- volcanic_pumice

## 1.4.3 MaterialType: CORAL_STONE
- reef_limestone

## 1.4.4 MaterialType: ALABASTER
- gypsum_alabaster

---

# 2. OPTIONAL EXTENSIONS (System-Ready Slots)

## 2.1 RegionTag (optional metadata)
- northern_europe
- alpine
- mediterranean
- iberian
- britannic
- scandinavian

## 2.2 StructuralRole (policy-driven)
- foundation
- wall_loadbearing
- vault
- roof_cladding
- decorative
- sculptural

## 2.3 QualityTier (culture-dependent)
- rough
- dressed
- ashlar
- monumental

---

# FINAL STRUCTURE (ABSTRAKT)

MaterialClass
  └── MaterialGroup
        └── MaterialType
              └── Variant
                    └── (RegionTag / QualityTier / StructuralRole as metadata)

---

Diese Hierarchie ist:
- geologisch korrekt
- historisch plausibel
- physikfähig
- renderfähig
- erweiterbar ohne Rewrite
