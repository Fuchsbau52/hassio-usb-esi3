# USB-ESI3 zu MQTT Add-on Dokumentation

## Übersicht

Dieses Add-on liest Energiemessdaten vom USB-ESI3 Gerät und publiziert sie via MQTT zu Home Assistant. Es unterstützt:
- **Strom-Sensoren** (ES-IEC mit SML, ES-LED mit S0)
- **Gas-Sensoren** (ES-LED mit S0)
- **Bis zu 3 Kanäle** gleichzeitig
- **Automatische Home Assistant Discovery**
- **Kanal-spezifische Offsets** für S0-Sensoren

## Installation

1. Füge dieses Repository zu deinen Home Assistant Add-on Repositories hinzu
2. Installiere das Add-on
3. Konfiguriere die Parameter
4. Starte das Add-on

## Konfiguration

### Basis-Einstellungen

#### Serieller Port
Der USB-Port des ESI3-Geräts (z.B. `/dev/ttyUSB0`)

**Tipp:** Nutze den Home Assistant Terminal und führe aus:
```bash
ls -la /dev/tty*
```
um verfügbare USB-Geräte zu sehen.

#### MQTT Einstellungen
- **MQTT Host:** IP-Adresse oder Hostname des MQTT Brokers (Standard: `core-mosquitto`)
- **MQTT Port:** Port des Brokers (Standard: `1883`)
- **MQTT User:** Benutzername für MQTT
- **MQTT Passwort:** Passwort für MQTT

### Offset-Einstellungen (Wichtig!)

Das USB-ESI3 unterstützt verschiedene Sensor-Typen:

#### ES-IEC (SML) Sensoren
Diese lesen **echte Zählerstände** direkt vom Smart Meter aus.
- ✅ **Kein Offset nötig!** → Setze auf `0.0`
- Die Werte sind bereits korrekt

#### ES-LED (S0) Sensoren
Diese zählen nur **Impulse** und starten bei 0.
- ❌ **Offset nötig!** → Setze auf deinen aktuellen Zählerstand
- Beispiel: Dein Gaszähler zeigt 3542 m³ → Offset: `3540.0`

### Kanal-Konfiguration

Die Offsets werden **pro Kanal** konfiguriert. Egal welcher Sensor an welchem Kanal steckt!

```yaml
# Beispiel 1: Kanal 1 = SML, Kanal 2 = Gas S0, Kanal 3 = Strom S0
channel_1_import_offset: 0.0      # ES-IEC (SML) → kein Offset
channel_1_export_offset: 0.0      # ES-IEC (SML) → kein Offset
channel_2_import_offset: 3540.0   # Gas ES-LED → Zählerstand
channel_3_import_offset: 4837.0   # Strom ES-LED → Zählerstand
channel_3_export_offset: 303.0    # Strom ES-LED → Einspeisung

# Beispiel 2: Beliebige Reihenfolge
channel_1_import_offset: 4837.0   # Strom S0 an Kanal 1
channel_1_export_offset: 303.0
channel_2_import_offset: 0.0      # SML an Kanal 2 → kein Offset
channel_2_export_offset: 0.0
channel_3_import_offset: 3540.0   # Gas S0 an Kanal 3
```

### Offset berechnen

**Für ES-LED (S0) Sensoren:**

1. Schaue auf deinen **echten Zähler**: z.B. `3542.456 m³`
2. Schaue im **Add-on Log** was das USB-ESI3 sendet: z.B. `2.123 m³`
3. **Berechne:** `3542.456 - 2.123 = 3540.333`
4. **Runde:** `3540.0` (auf ganze Zahlen oder 1 Dezimalstelle)
5. **Trage ein:** `channel_2_import_offset: 3540.0`

**Ergebnis:** Home Assistant zeigt `3542.123 m³` ✅

### Erweiterte Einstellungen

#### Device Name
Anzeigename des Geräts in Home Assistant (Standard: `USB-ESI3`)

#### Base Topic
MQTT Topic-Präfix (Standard: `sensors/usb-esi3`)

#### Log Level
Detailgrad der Logs:
- `info` - Normal (empfohlen)
- `debug` - Sehr detailliert (für Fehlersuche)
- `warning` - Nur Warnungen
- `error` - Nur Fehler

## Sensoren in Home Assistant

Nach dem Start werden automatisch Sensoren erstellt:

### Strom (Electricity)
- **Power** - Aktuelle Leistung in W
- **Energy Import** - Bezug gesamt in kWh
- **Energy Export** - Einspeisung gesamt in kWh

### Gas
- **Volume Import** - Verbrauch gesamt in m³
- **Momentary Use** - Aktueller Verbrauch in m³/h

### Benennung
Die Sensoren heißen:
- `Electricity Channel 1 Power`
- `Gas Channel 2 Volume Import`
- `Electricity Channel 3 Energy Import`

So kannst du immer sehen, welcher Sensor an welchem Kanal ist.

## Energie Dashboard

Die Sensoren sind für das Home Assistant Energie Dashboard optimiert:

1. Gehe zu: **Einstellungen** → **Dashboards** → **Energie**
2. **Stromnetz:**
   - Netzbezug: Wähle den `Energy Import` Sensor
   - Netzeinspeisung: Wähle den `Energy Export` Sensor
3. **Gas:**
   - Gasverbrauch: Wähle den `Volume Import` Sensor
   - Umrechnungsfaktor: z.B. `10.3 kWh/m³` (je nach Brennwert)
4. **Speichern**

## Troubleshooting

### USB-Gerät nicht gefunden
**Symptom:** `USB-Gerät /dev/ttyUSB0 nicht gefunden`

**Lösung:**
1. Prüfe mit `ls -la /dev/tty*` welche Geräte verfügbar sind
2. Passe `serial_port` in der Konfiguration an
3. Stelle sicher, dass das USB-ESI3 korrekt angeschlossen ist

### MQTT Verbindung schlägt fehl
**Symptom:** `MQTT Verbindungsfehler - Return Code: 5`

**Lösung:**
1. Prüfe ob der Mosquitto Broker läuft
2. Prüfe Benutzername und Passwort in der Konfiguration
3. Teste die Verbindung mit einem MQTT Client

### Werte sind falsch
**Symptom:** Werte sind zu hoch oder zu niedrig

**Lösung für ES-LED (S0) Sensoren:**
1. Prüfe den Offset in der Konfiguration
2. Berechne neu: `echter_zählerstand - usb_esi3_wert`
3. Aktualisiere die Konfiguration
4. Starte das Add-on neu

**ES-IEC (SML) Sensoren brauchen keinen Offset!**

### Sensor erscheint nicht im Energie Dashboard
**Symptom:** Sensor wird nicht zur Auswahl angeboten

**Lösung:**
1. Warte 1-2 Stunden (Home Assistant sammelt Statistiken)
2. Prüfe in **Entwicklerwerkzeuge** → **Statistiken**
3. Stelle sicher, dass der Sensor `state_class: total_increasing` hat

### Alte Sensoren mit doppeltem Namen
**Symptom:** `USB-ESI3 USB-ESI3 electricity Kanal 1 power`

**Lösung:**
1. Dies war ein Bug in älteren Versionen (< 1.2.0)
2. Neue Sensoren haben saubere Namen: `Electricity Channel 1 Power`
3. Lösche alte Sensoren manuell:
   - **Einstellungen** → **Geräte & Dienste** → **MQTT**
   - Suche nach "USB-ESI3 USB-ESI3"
   - Klicke auf jeden → **Löschen**

## Logs einsehen

Im Add-on-Tab unter **"Log"** siehst du detaillierte Logs mit Zeitstempeln:

```
2025-12-19 20:05:53 [INFO] usb_esi3: ✓ MQTT erfolgreich verbunden
2025-12-19 20:05:53 [INFO] usb_esi3: ✓ Serieller Port erfolgreich geöffnet
2025-12-19 20:05:53 [DEBUG] usb_esi3: Connector 1 (electricity): {'power': 366.0, 'energry_import': 483.77}
2025-12-19 20:05:53 [INFO] usb_esi3: ✓ MQTT → Connector 1: {"power": 366.0, "energry_import": 483.77}
```

**Tipp:** Setze `log_level: debug` für maximale Details bei Problemen.

## Statistiken

Das Add-on zeigt alle 5 Minuten Statistiken:

```
============================================================
STATISTIKEN:
  Laufzeit: 1:23:45
  Zeilen verarbeitet: 5000
  Zeilen ignoriert: 12
  MQTT publiziert: 4988
  MQTT Fehler: 0
  Serielle Fehler: 0
============================================================
```

## Support & Updates

- **GitHub:** https://github.com/Fuchsbau52/hassio-usb-esi3
- **Issues:** Bei Problemen öffne ein GitHub Issue
- **Updates:** Erscheinen automatisch im Add-on Store

## Changelog

### Version 1.4.0
- ✨ Kanal-spezifische Offsets (statt global)
- ✨ Unterstützung für beliebige Sensor-Reihenfolge
- ✨ Separate Offsets für jeden Kanal (1, 2, 3)
- 📝 Verbesserte Dokumentation

### Version 1.3.0
- ✨ Offset-Unterstützung für Startwerte
- 📝 Gas- und Strom-Offsets konfigurierbar

### Version 1.2.0
- ✨ Saubere Sensor-Namen ohne Dopplung
- ✨ Englische Bezeichnungen (Channel statt Kanal)

### Version 1.1.0
- ✨ Korrekte Umrechnungsfaktoren (÷100, ÷10000)
- 🐛 Bugfix: Power und Energy Werte

### Version 1.0.0
- 🎉 Initiales Release
- ✨ USB-ESI3 Unterstützung
- ✨ Home Assistant MQTT Discovery
- ✨ Detailliertes Logging
