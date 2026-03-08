## Vorläufige Architekturentscheidungen

1. `schema_version = 4` ist die aktuelle operative Wahrheit.
2. `schema_version = 3` ist Legacy-/Übergangspfad und muss aus kanonischen Prüfpfaden verschwinden.
3. `validate_frameplan_langhaus.py` ist ein Mischmodul aus Schema-, Domain- und Type-Regeln.
4. `frameplan_contract.py` und `frameplan_checks.py` sind nur dann haltbar, wenn sie auf Schema 4 vereinheitlicht und klar getrennt werden.
5. Dokumentation und Code sind aktuell nicht konsistent; Tier-1-Dokumente müssen nach der Code-Konsolidierung nachgezogen werden.
