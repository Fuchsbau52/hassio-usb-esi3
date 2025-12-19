# -*- coding: utf-8 -*-

"""
USB-ESI3 -> MQTT Publisher für Home Assistant Add-on
Mit Umgebungsvariablen-Konfiguration und verbessertem Logging
"""

import os
import re
import json
import time
import logging
import signal
import threading
from typing import Dict, Tuple, Optional
from datetime import datetime

import serial
from paho.mqtt import client as mqtt_client

# -------------------------
# Konfiguration aus Umgebungsvariablen
# -------------------------

SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUDRATE = int(os.getenv("BAUDRATE", "115200"))
SERIAL_TIMEOUT = 1.0

MQTT_HOST = os.getenv("MQTT_HOST", "core-mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASS = os.getenv("MQTT_PASS", "")

DEVICE_NAME = os.getenv("DEVICE_NAME", "USB-ESI3")
DEVICE_ID = "usb-esi3"
BASE_TOPIC = os.getenv("BASE_TOPIC", "sensors/usb-esi3")
STATUS_TOPIC = f"{BASE_TOPIC}/status"
QOS = 1
RETAIN_STATE = True
RETAIN_DISCOVERY = True

# Log Level
LOG_LEVEL = os.getenv("LOG_LEVEL", "info").upper()

UNITS_ELECTRICITY = {
    "power": "W",
    "energy_import": "kWh",
    "energry_import": "kWh",  # Tippfehler im USB-ESI3 Gerät
    "energy_export": "kWh",
    "energry_export": "kWh",  # Tippfehler im USB-ESI3 Gerät
    "energy_import_nt": "kWh",
}
UNITS_GAS = {
    "volume_import": "m³",
    "momentary_use": "m³/h",
}

HA_META = {
    "electricity": {
        "power": {"device_class": "power", "state_class": "measurement"},
        "energy_import": {"device_class": "energy", "state_class": "total_increasing"},
        "energry_import": {"device_class": "energy", "state_class": "total_increasing"},  # Tippfehler
        "energy_export": {"device_class": "energy", "state_class": "total_increasing"},
        "energry_export": {"device_class": "energy", "state_class": "total_increasing"},  # Tippfehler
        "energy_import_nt": {"device_class": "energy", "state_class": "total_increasing"},
    },
    "gas": {
        "volume_import": {"device_class": "gas", "state_class": "total_increasing"},
        "momentary_use": {"device_class": "gas", "state_class": "measurement"},
    },
}

# -------------------------
# Logging Setup mit Zeitstempeln
# -------------------------

class CustomFormatter(logging.Formatter):
    """Farbige Logs für bessere Lesbarkeit"""
    
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    def __init__(self):
        super().__init__()
        self.fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        self.datefmt = "%Y-%m-%d %H:%M:%S"
        
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)

# Logger konfigurieren
handler = logging.StreamHandler()
handler.setFormatter(CustomFormatter())

log = logging.getLogger("usb_esi3")
log.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))
log.addHandler(handler)

# Regex
HEADER_RE = re.compile(
    r"^\s*Connector\s+(\d+)\s*:\s*(electricity|gas)\s*;?\s*(.*)$",
    re.IGNORECASE
)

# Stop Event
stop_event = threading.Event()
_discovered: Dict[Tuple[int, str], Dict[str, bool]] = {}

# Statistiken
stats = {
    "start_time": datetime.now(),
    "lines_processed": 0,
    "lines_ignored": 0,
    "mqtt_published": 0,
    "mqtt_errors": 0,
    "serial_errors": 0,
}

# -------------------------
# Parser
# -------------------------

def parse_line(line: str) -> Optional[Tuple[int, str, Dict[str, float]]]:
    """Parst eine Zeile vom USB-ESI3"""
    line = line.strip()
    if not line:
        return None

    m = HEADER_RE.match(line)
    if not m:
        return None

    conn_idx = int(m.group(1))
    meter_type = m.group(2).lower()
    tail = m.group(3) or ""

    data: Dict[str, float] = {}
    parts = [p.strip() for p in tail.split(";") if p.strip()]
    for part in parts:
        if "=" not in part:
            continue
        key, val = part.split("=", 1)
        key = key.strip()
        val = val.strip()
        try:
            num = float(val)
            data[key] = num
        except ValueError:
            data[key] = val

    return (conn_idx, meter_type, data)

def convert_and_round_values(meter_type: str, data: Dict[str, float]) -> Dict[str, float]:
    """
    Konvertiert und rundet Werte basierend auf dem Meter-Typ
    - power: mW -> W (Faktor 1000) und auf 1 Dezimalstelle
    - energy_import/export: Wh -> kWh (Faktor 1000) und auf 2 Dezimalstellen
    """
    converted = {}
    
    for key, value in data.items():
        if not isinstance(value, (int, float)):
            converted[key] = value
            continue
            
        if meter_type == "electricity":
            if key == "power":
                # Leistung: mW -> W (durch 1000)
                converted[key] = round(value / 100, 1)
            elif key in ["energy_import", "energy_export", "energy_import_nt", "energry_import", "energry_export"]:
                # Energie: Wh -> kWh (durch 1000)
                converted[key] = round(value / 10000, 2)
            else:
                # Andere Werte: 2 Dezimalstellen
                converted[key] = round(value, 2)
        elif meter_type == "gas":
            if key == "volume_import":
                # Gas-Volumen: m³ (bereits korrekte Einheit, nur runden)
                converted[key] = round(value, 3)
            elif key == "momentary_use":
                # Momentaner Verbrauch
                converted[key] = round(value, 3)
            else:
                converted[key] = round(value, 3)
        else:
            converted[key] = round(value, 2)
    
    return converted

# -------------------------
# MQTT Client
# -------------------------

def make_mqtt_client(client_id: str) -> mqtt_client.Client:
    log.info("MQTT Client wird erstellt...")
    
    # Kompatibilität für paho-mqtt < 2.0 und >= 2.0
    try:
        # Versuche neue API (paho-mqtt >= 2.0)
        client = mqtt_client.Client(
            mqtt_client.CallbackAPIVersion.VERSION1, 
            client_id=client_id, 
            clean_session=True
        )
        log.debug("Nutze paho-mqtt >= 2.0 API")
    except AttributeError:
        # Fallback auf alte API (paho-mqtt < 2.0)
        client = mqtt_client.Client(
            client_id=client_id, 
            clean_session=True
        )
        log.debug("Nutze paho-mqtt < 2.0 API")
    
    if MQTT_USER:
        log.info(f"MQTT Authentifizierung für Benutzer: {MQTT_USER}")
        client.username_pw_set(MQTT_USER, MQTT_PASS or "")

    client.will_set(STATUS_TOPIC, payload="offline", qos=QOS, retain=True)

    def on_connect(c, userdata, flags, rc):
        if rc == 0:
            log.info("✓ MQTT erfolgreich verbunden")
            c.publish(STATUS_TOPIC, "online", qos=QOS, retain=True)
        else:
            log.error(f"✗ MQTT Verbindungsfehler - Return Code: {rc}")

    def on_disconnect(c, userdata, rc):
        if rc == 0:
            log.info("MQTT sauber getrennt")
        else:
            log.warning(f"MQTT Verbindung unterbrochen - Return Code: {rc}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    log.info(f"Verbinde zu MQTT Broker: {MQTT_HOST}:{MQTT_PORT}")
    try:
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
        log.info("MQTT Verbindung initiiert")
    except Exception as e:
        log.error(f"MQTT Verbindung fehlgeschlagen: {e}")
        raise
    
    return client

# -------------------------
# Home Assistant Discovery
# -------------------------

def device_info() -> Dict:
    return {
        "identifiers": [DEVICE_ID],
        "name": DEVICE_NAME,
        "manufacturer": "USB-ESI3",
        "model": "Energy/Gas Serial Interface",
    }

def publish_discovery_for_keys(
    client: mqtt_client.Client,
    conn_idx: int,
    meter_type: str,
    keys: Dict[str, float]
) -> None:
    """Publiziert HA Discovery Payloads für neue Keys"""
    state_topic = f"{BASE_TOPIC}/connector/{conn_idx}/state"
    published_for_conn = _discovered.setdefault((conn_idx, meter_type), {})

    unit_map = UNITS_ELECTRICITY if meter_type == "electricity" else UNITS_GAS

    for key in keys.keys():
        if published_for_conn.get(key):
            continue

        unique_id = f"{DEVICE_ID}_conn{conn_idx}_{key}"
        discovery_topic = f"homeassistant/sensor/{unique_id}/config"

        payload = {
            "name": f"{DEVICE_NAME} {meter_type} Kanal {conn_idx} {key}",
            "unique_id": unique_id,
            "state_topic": state_topic,
            "value_template": f"{{{{ value_json.{key} }}}}",
            "availability_topic": STATUS_TOPIC,
            "payload_available": "online",
            "payload_not_available": "offline",
            "device": device_info(),
        }

        unit = unit_map.get(key)
        if unit:
            payload["unit_of_measurement"] = unit

        meta = HA_META.get(meter_type, {}).get(key, {})
        payload.update(meta)

        client.publish(discovery_topic, json.dumps(payload), qos=QOS, retain=RETAIN_DISCOVERY)
        log.info(f"✓ Discovery: Connector {conn_idx}, {meter_type}, Key '{key}'")
        published_for_conn[key] = True

# -------------------------
# Serielle Verbindung
# -------------------------

def open_serial() -> Optional[serial.Serial]:
    try:
        log.info(f"Öffne seriellen Port: {SERIAL_PORT} @ {BAUDRATE} Baud")
        ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=SERIAL_TIMEOUT)
        log.info(f"✓ Serieller Port erfolgreich geöffnet: {ser.port}")
        return ser
    except Exception as e:
        log.error(f"✗ Serieller Port konnte nicht geöffnet werden: {e}")
        stats["serial_errors"] += 1
        return None

# -------------------------
# Statistiken ausgeben
# -------------------------

def log_statistics():
    """Gibt Statistiken aus"""
    runtime = datetime.now() - stats["start_time"]
    log.info("=" * 60)
    log.info("STATISTIKEN:")
    log.info(f"  Laufzeit: {runtime}")
    log.info(f"  Zeilen verarbeitet: {stats['lines_processed']}")
    log.info(f"  Zeilen ignoriert: {stats['lines_ignored']}")
    log.info(f"  MQTT publiziert: {stats['mqtt_published']}")
    log.info(f"  MQTT Fehler: {stats['mqtt_errors']}")
    log.info(f"  Serielle Fehler: {stats['serial_errors']}")
    log.info("=" * 60)

# -------------------------
# Hauptlogik
# -------------------------

def run_loop() -> None:
    log.info("=" * 60)
    log.info("USB-ESI3 zu MQTT Bridge gestartet")
    log.info("=" * 60)
    log.info(f"Konfiguration:")
    log.info(f"  Serieller Port: {SERIAL_PORT}")
    log.info(f"  Baudrate: {BAUDRATE}")
    log.info(f"  MQTT Broker: {MQTT_HOST}:{MQTT_PORT}")
    log.info(f"  Base Topic: {BASE_TOPIC}")
    log.info(f"  Device Name: {DEVICE_NAME}")
    log.info(f"  Log Level: {LOG_LEVEL}")
    log.info("=" * 60)
    
    client = make_mqtt_client(client_id=f"{DEVICE_ID}_publisher")
    client.loop_start()

    ser = open_serial()
    last_serial_attempt = time.time()
    last_stats_log = time.time()

    try:
        while not stop_event.is_set():
            # Statistiken alle 5 Minuten
            if time.time() - last_stats_log >= 300:
                log_statistics()
                last_stats_log = time.time()
            
            # Serielle Verbindung wiederherstellen
            if ser is None and (time.time() - last_serial_attempt) >= 3.0:
                last_serial_attempt = time.time()
                log.info("Versuche serielle Verbindung wiederherzustellen...")
                ser = open_serial()

            if ser is None:
                time.sleep(0.2)
                continue

            try:
                raw_bytes = ser.readline()
                if not raw_bytes:
                    continue

                raw = raw_bytes.decode(errors="ignore").strip()
                if not raw:
                    continue

                parsed = parse_line(raw)
                if not parsed:
                    stats["lines_ignored"] += 1
                    log.debug(f"Zeile ignoriert: {raw}")
                    continue

                stats["lines_processed"] += 1
                conn_idx, meter_type, data = parsed
                
                if not data:
                    continue

                # Werte konvertieren und runden
                data = convert_and_round_values(meter_type, data)

                log.debug(f"Connector {conn_idx} ({meter_type}): {data}")

                # Discovery
                publish_discovery_for_keys(client, conn_idx, meter_type, data)

                # State publizieren
                state_topic = f"{BASE_TOPIC}/connector/{conn_idx}/state"
                payload = json.dumps(data)
                res = client.publish(state_topic, payload, qos=QOS, retain=RETAIN_STATE)
                rc = res[0] if isinstance(res, tuple) else getattr(res, "rc", 0)
                
                if rc == 0:
                    stats["mqtt_published"] += 1
                    log.info(f"✓ MQTT → Connector {conn_idx}: {payload}")
                else:
                    stats["mqtt_errors"] += 1
                    log.error(f"✗ MQTT Publish fehlgeschlagen (rc={rc})")

                time.sleep(0.05)

            except serial.SerialException as e:
                log.error(f"✗ Serielle Ausnahme: {e}")
                stats["serial_errors"] += 1
                try:
                    ser.close()
                except Exception:
                    pass
                ser = None
                time.sleep(0.5)

    finally:
        log.info("Beende Programm...")
        log_statistics()
        
        try:
            if ser is not None:
                ser.close()
                log.info("✓ Serieller Port geschlossen")
        except Exception as e:
            log.error(f"Fehler beim Schließen des seriellen Ports: {e}")
        
        client.loop_stop()
        client.disconnect()
        log.info("✓ MQTT Verbindung beendet")
        log.info("Programm sauber beendet")

def main():
    def _handle_signal(sig, frame):
        log.info(f"Signal empfangen: {sig} - Beende Programm...")
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    run_loop()

if __name__ == "__main__":
    main()
