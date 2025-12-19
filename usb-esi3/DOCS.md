# USB-ESI3 zu MQTT Add-on Dokumentation

## Installation

1. Füge dieses Repository zu deinen Home Assistant Add-on Repositories hinzu
2. Installiere das Add-on
3. Konfiguriere die Parameter
4. Starte das Add-on

## Konfiguration

### Serieller Port
Der USB-Port des ESI3-Geräts (z.B. `/dev/ttyUSB0`)

**Tipp:** Nutze `ha hardware info` um verfügbare USB-Geräte zu sehen

### MQTT Einstellungen
- **MQTT Host:** IP-Adresse oder Hostname des MQTT Brokers (Standard: `core-mosquitto`)
- **MQTT Port:** Port des Brokers (Standard: `1883`)
- **MQTT User:** Benutzername für MQTT
- **MQTT Passwort:** Passwort für MQTT

### Erweiterte Einstellungen
- **Device Name:** Anzeigename des Geräts in Home Assistant
- **Base Topic:** MQTT Topic-Präfix
- **Log Level:** Detailgrad der Logs (`debug`, `info`, `warning`, `error`)

## Troubleshooting

### USB-Gerät nicht gefunden
Prüfe mit `ha hardware info` welche USB-Geräte erkannt werden.

### MQTT Verbindung schlägt fehl
- Prüfe ob der Mosquitto Broker läuft
- Prüfe Benutzername und Passwort
- Prüfe Netzwerkverbindung

### Logs einsehen
Im Add-on-Tab unter "Log" kannst du die detaillierten Logs mit Zeitstempeln sehen.
