# Changelog

## [1.4.0] - 2024-12-20
### Added
- Kanal-spezifische Offsets (channel_1/2/3_import/export_offset)
- Unterstützung für beliebige Sensor-Reihenfolge an Kanälen
- Separate Offset-Konfiguration für jeden Kanal

### Changed
- Offsets sind jetzt pro Kanal statt global
- Verbesserte Dokumentation mit ausführlichen Beispielen
- Logging zeigt nur konfigurierte Offsets an (> 0)

### Migration from 1.3.0
- `gas_volume_offset` → `channel_2_import_offset` (wenn Gas an Kanal 2)
- `electricity_import_offset` → `channel_1_import_offset` (wenn Strom an Kanal 1)
- `electricity_export_offset` → `channel_1_export_offset` (wenn Strom an Kanal 1)

## [1.3.0] - 2024-12-20
### Added
- Offset-Konfiguration für Startwerte
- `gas_volume_offset` für Gas-Zählerstand
- `electricity_import_offset` für Strom-Bezug
- `electricity_export_offset` für Strom-Einspeisung

### Changed
- Logging zeigt konfigurierte Offsets beim Start

## [1.2.0] - 2024-12-19
### Fixed
- Sensor-Namen ohne Dopplung (vorher: "USB-ESI3 USB-ESI3 electricity...")
- Englische Bezeichnungen konsistent (Channel statt Kanal im Namen)

### Changed
- Sensor-Namen: "Electricity Channel 1 Power" statt "USB-ESI3 USB-ESI3 electricity Kanal 1 power"
- Automatische Korrektur: "energry" → "energy" in Sensor-Namen

## [1.1.0] - 2024-12-19
### Fixed
- Korrekte Umrechnungsfaktoren für Power (÷100 statt ×1000)
- Korrekte Umrechnungsfaktoren für Energy (÷10000)
- Power-Werte jetzt korrekt in Watt
- Energy-Werte jetzt korrekt in kWh

## [1.0.9] - 2024-12-19
### Fixed
- Separate Behandlung von energy_import und energy_export
- energy_import: ÷10, energy_export: keine Änderung

## [1.0.8] - 2024-12-19
### Fixed
- Energie-Werte durch 10 teilen für korrekte kWh-Anzeige

## [1.0.7] - 2024-12-19
### Fixed
- Power: ×1000 für korrekte Watt-Anzeige
- Energy: ohne Änderung

## [1.0.6] - 2024-12-19
### Fixed
- Umrechnungsfaktoren angepasst

## [1.0.5] - 2024-12-19
### Added
- Erste Version mit Werte-Umrechnung
- Power: ×10
- Energy: ÷1000

## [1.0.4] - 2024-12-19
### Fixed
- MQTT Client Kompatibilität für paho-mqtt < 2.0

### Changed
- Fallback für ältere paho-mqtt Versionen ohne CallbackAPIVersion

## [1.0.3] - 2024-12-19
### Fixed
- config.yaml URL und zusätzliche Felder

## [1.0.2] - 2024-12-19
### Fixed
- Dockerfile ohne image: Zeile für lokalen Build

## [1.0.1] - 2024-12-19
### Fixed
- run.sh mit jq statt bashio für robustere Konfiguration

## [1.0.0] - 2024-12-19
### Added
- Initiales Release
- USB-ESI3 Unterstützung (Electricity & Gas)
- Home Assistant MQTT Discovery
- Automatische Sensor-Erstellung
- Konfigurierbare Parameter (Serial Port, MQTT, Log Level)
- Detailliertes Logging mit Zeitstempeln
- Statistiken alle 5 Minuten
- Sauberes Signal-Handling (SIGINT/SIGTERM)
- Support für energry_* Tippfehler im USB-ESI3
- Gas device_class für Energie Dashboard
