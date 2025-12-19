# Home Assistant Add-on: USB-ESI3 zu MQTT

Dieses Add-on liest Daten vom USB-ESI3 Energiemessgerät und publiziert sie via MQTT zu Home Assistant.

## Installation

1. Füge dieses Repository zu deinen Home Assistant Add-on Repositories hinzu:
   - Öffne Home Assistant
   - Gehe zu **Einstellungen** → **Add-ons** → **Add-on Store**
   - Klicke auf die drei Punkte oben rechts → **Repositories**
   - Füge die URL hinzu: `https://github.com/DEIN-USERNAME/hassio-usb-esi3`

2. Suche nach "USB-ESI3 zu MQTT" im Add-on Store
3. Klicke auf **Installieren**
4. Konfiguriere das Add-on (siehe unten)
5. Starte das Add-on

## Konfiguration

Beispielkonfiguration:

```yaml
serial_port: "/dev/ttyUSB0"
baudrate: 115200
mqtt_host: "core-mosquitto"
mqtt_port: 1883
mqtt_user: "dein_mqtt_user"
mqtt_pass: "dein_mqtt_passwort"
device_name: "USB-ESI3"
base_topic: "sensors/usb-esi3"
log_level: "info"
```

## Support

Bei Problemen öffne bitte ein Issue auf GitHub.
```

### Schritt 4: Dateien auf GitHub hochladen

1. Lade alle erstellten Dateien in dein GitHub Repository hoch
2. Beachte die korrekte Ordnerstruktur

### Schritt 5: Add-on in Home Assistant installieren

1. Öffne Home Assistant
2. Gehe zu **Einstellungen** → **Add-ons** → **Add-on Store**
3. Klicke auf die **drei Punkte** oben rechts
4. Wähle **Repositories**
5. Füge deine Repository-URL hinzu: `https://github.com/DEIN-USERNAME/hassio-usb-esi3`
6. Klicke auf **Hinzufügen**

### Schritt 6: Add-on konfigurieren und starten

1. Suche nach "USB-ESI3 zu MQTT" im Add-on Store
2. Klicke auf **Installieren**
3. Nach der Installation öffne die **Konfiguration**:
   - Passe den USB-Port an (z.B. `/dev/ttyUSB0`)
   - Trage MQTT-Zugangsdaten ein
   - Wähle Log Level (für Debugging: `debug`)
4. Klicke auf **Speichern**
5. Gehe zum Tab **Info**
6. Klicke auf **Starten**

### Schritt 7: Logs überprüfen

1. Gehe zum Tab **Log**
2. Du siehst nun detaillierte Logs mit Zeitstempeln:
   ```
   2024-12-19 14:23:45 [INFO] usb_esi3: USB-ESI3 zu MQTT Bridge gestartet
   2024-12-19 14:23:45 [INFO] usb_esi3: Serieller Port: /dev/ttyUSB0
   2024-12-19 14:23:46 [INFO] usb_esi3: ✓ MQTT erfolgreich verbunden
   ```

### Schritt 8: Geräte in Home Assistant prüfen

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke auf **MQTT**
3. Dein USB-ESI3 Gerät sollte automatisch erscheinen
4. Alle Sensoren werden automatisch angelegt

## Debugging-Tipps

### USB-Port herausfinden

Führe im Home Assistant Terminal aus:
```bash
ha hardware info
```

### MQTT Verbindung testen

Im Log sollte stehen:
```
✓ MQTT erfolgreich verbunden
```

Falls nicht, prüfe:
- Läuft der Mosquitto Broker?
- Sind Benutzername/Passwort korrekt?

### Ausführliche Logs

Setze `log_level: "debug"` in der Konfiguration für maximale Details.

## Häufige Fehler und Lösungen

| Fehler | Lösung |
|--------|--------|
| "USB-Gerät nicht gefunden" | USB-Port in Konfiguration anpassen |
| "MQTT Verbindungsfehler" | Broker läuft? Zugangsdaten korrekt? |
| "Permission denied" | Add-on neu starten |

## Updates

Um das Add-on zu aktualisieren:
1. Ändere die Version in `config.yaml`
2. Update `CHANGELOG.md`
3. Pushe zu GitHub
4. In Home Assistant auf "Update" klicken
