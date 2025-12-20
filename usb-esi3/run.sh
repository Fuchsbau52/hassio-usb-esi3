#!/usr/bin/env bashio

set -e

CONFIG_PATH=/data/options.json

# Konfiguration aus Home Assistant lesen
export SERIAL_PORT=$(jq --raw-output '.serial_port // "/dev/ttyUSB0"' $CONFIG_PATH)
export BAUDRATE=$(jq --raw-output '.baudrate // 115200' $CONFIG_PATH)
export MQTT_HOST=$(jq --raw-output '.mqtt_host // "core-mosquitto"' $CONFIG_PATH)
export MQTT_PORT=$(jq --raw-output '.mqtt_port // 1883' $CONFIG_PATH)
export MQTT_USER=$(jq --raw-output '.mqtt_user // ""' $CONFIG_PATH)
export MQTT_PASS=$(jq --raw-output '.mqtt_pass // ""' $CONFIG_PATH)
export DEVICE_NAME=$(jq --raw-output '.device_name // "USB-ESI3"' $CONFIG_PATH)
export BASE_TOPIC=$(jq --raw-output '.base_topic // "sensors/usb-esi3"' $CONFIG_PATH)
export LOG_LEVEL=$(jq --raw-output '.log_level // "info"' $CONFIG_PATH)

# Offsets
export GAS_VOLUME_OFFSET=$(jq --raw-output '.gas_volume_offset // 0.0' $CONFIG_PATH)
export ELECTRICITY_IMPORT_OFFSET=$(jq --raw-output '.electricity_import_offset // 0.0' $CONFIG_PATH)
export ELECTRICITY_EXPORT_OFFSET=$(jq --raw-output '.electricity_export_offset // 0.0' $CONFIG_PATH)

# Logging
echo "=========================================="
echo "USB-ESI3 zu MQTT Add-on wird gestartet..."
echo "=========================================="
echo "Serieller Port: ${SERIAL_PORT}"
echo "Baudrate: ${BAUDRATE}"
echo "MQTT Broker: ${MQTT_HOST}:${MQTT_PORT}"
echo "MQTT Benutzer: ${MQTT_USER}"
echo "Base Topic: ${BASE_TOPIC}"
echo "Log Level: ${LOG_LEVEL}"
echo "Offsets:"
echo "  Gas Volume: +${GAS_VOLUME_OFFSET} m³"
echo "  Electricity Import: +${ELECTRICITY_IMPORT_OFFSET} kWh"
echo "  Electricity Export: +${ELECTRICITY_EXPORT_OFFSET} kWh"
echo "=========================================="

# Prüfe ob USB-Gerät existiert
if [ ! -e "${SERIAL_PORT}" ]; then
    echo "WARNUNG: USB-Gerät ${SERIAL_PORT} nicht gefunden!"
    echo "Verfügbare Geräte:"
    ls -la /dev/tty* 2>/dev/null || echo "Keine USB-Geräte gefunden"
    echo ""
fi

# Python Skript starten
echo "Starte Python Skript..."
exec python3 /app/usb-esi3.py
