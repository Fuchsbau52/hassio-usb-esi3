# Home Assistant Add-on: USB-ESI3 zu MQTT

![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)
![Supports aarch64](https://img.shields.io/badge/aarch64-yes-green.svg)
![Supports amd64](https://img.shields.io/badge/amd64-yes-green.svg)
![Supports armv7](https://img.shields.io/badge/armv7-yes-green.svg)

Liest Energiemessdaten vom USB-ESI3 Gerät und publiziert sie via MQTT zu Home Assistant mit automatischer Discovery.

## Features

✨ **Automatische Sensor-Erkennung** - Home Assistant Discovery für alle Sensoren  
⚡ **Strom & Gas** - Unterstützt ES-IEC (SML), ES-LED (S0) und ES-GAS-2 Sensoren  
🔧 **Kanal-spezifische Offsets** - Individuelle Startwerte für jeden Kanal  
📊 **Energie Dashboard** - Optimiert für das HA Energie Dashboard  
📝 **Detailliertes Logging** - Zeitstempel, Statistiken, Debug-Modus  
🔄 **Flexibel** - Sensoren können in beliebiger Reihenfolge angeschlossen werden  

## Unterstützte Sensoren

### ES-IEC (SML)
Liest echte Zählerstände direkt vom Smart Meter
- ✅ Kein Offset nötig
- ✅ Automatische Erkennung aller Werte
- ✅ Bezug und Einspeisung

### ES-LED (S0)
Zählt Impulse von S0-Schnittstellen
- ⚙️ Offset für Startstand konfigurierbar
- ✅ Gas und Strom
- ✅ Beliebige Impulswerte

### ES-GAS-2
Zählt Impulse von der Schnittstelle
- ⚙️ Offset für Startstand konfigurierbar
- ✅ Gas und Strom
- ✅ Beliebige Impulswerte

## Installation

1. Füge dieses Repository zu deinen Home Assistant Add-on Repositories hinzu:
   - Öffne Home Assistant
   - Gehe zu **Einstellungen** → **Add-ons** → **Add-on Store**
   - Klicke auf die drei Punkte oben rechts → **Repositories**
   - Füge die URL hinzu: `https://github.com/Fuchsbau52/hassio-usb-esi3`

2. Suche nach "USB-ESI3 zu MQTT" im Add-on Store
3. Klicke auf **Installieren**
4. Konfiguriere das Add-on (siehe unten)
5. Starte das Add-on

## Konfiguration

### Minimal-Konfiguration

```yaml
serial_port: "/dev/ttyUSB0"
mqtt_user: "dein_mqtt_user"
mqtt_pass: "dein_mqtt_passwort"
```

### Vollständige Konfiguration

```yaml
serial_port: "/dev/ttyUSB0"
baudrate: 115200
mqtt_host: "core-mosquitto"
mqtt_port: 1883
mqtt_user: "mqtt"
mqtt_pass: "dein_passwort"
device_name: "USB-ESI3"
base_topic: "sensors/usb-esi3"
log_level: "info"

# Offsets für S0-Sensoren (ES-LED und ES-GAS-2)
# ES-IEC (SML) Sensoren brauchen keinen Offset!
channel_1_import_offset: 0.0      # Kanal 1: Strom SML → kein Offset
channel_1_export_offset: 0.0
channel_2_import_offset: 3540.0   # Kanal 2: Gas → Zählerstand
channel_3_import_offset: 0.0      # Kanal 3: nicht verwendet
channel_3_export_offset: 0.0
```

### Offset-Beispiele

**Szenario 1: SML + Gas**
```yaml
channel_1_import_offset: 0.0      # ES-IEC (SML) an Kanal 1
channel_1_export_offset: 0.0
channel_2_import_offset: 3542.5   # Gas ES-GAS-2 an Kanal 2
```

**Szenario 2: Alle S0 Sensoren**
```yaml
channel_1_import_offset: 4837.0   # Strom ES-LED an Kanal 1
channel_1_export_offset: 303.0
channel_2_import_offset: 3542.0   # Gas ES-GAS-2 an Kanal 2
channel_3_import_offset: 1234.0   # Weiterer ES-LED an Kanal 3
```

**Szenario 3: Beliebige Reihenfolge**
```yaml
channel_1_import_offset: 3542.0   # Gas an Kanal 1
channel_2_import_offset: 0.0      # SML an Kanal 2 → kein Offset!
channel_3_import_offset: 4837.0   # Strom S0 an Kanal 3
```

## Sensoren in Home Assistant

Nach dem Start werden automatisch erstellt:

### Strom (Electricity)
- `Electricity Channel X Power` (W)
- `Electricity Channel X Energy Import` (kWh)
- `Electricity Channel X Energy Export` (kWh)

### Gas
- `Gas Channel X Volume Import` (m³)
- `Gas Channel X Momentary Use` (m³/h)

## Energie Dashboard

Die Sensoren sind optimiert für das HA Energie Dashboard:

1. **Einstellungen** → **Dashboards** → **Energie**
2. **Stromnetz:** Wähle Energy Import/Export Sensoren
3. **Gas:** Wähle Volume Import Sensor (Umrechnung: z.B. 10.3 kWh/m³)

## Support

- **Dokumentation:** Siehe DOCS.md im Add-on
- **Issues:** https://github.com/Fuchsbau52/hassio-usb-esi3/issues
- **Changelog:** Siehe CHANGELOG.md

## Lizenz

MIT License - siehe LICENSE Datei

## Credits

Entwickelt für die Home Assistant Community 💚
```
