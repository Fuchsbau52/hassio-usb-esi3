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

# Offsets pro Kanal
export CHANNEL_1_IMPORT_OFFSET=$(jq --raw-output '.channel_1_import_offset // 0.0' $CONFIG_PATH)
export CHANNEL_1_EXPORT_OFFSET=$(jq --raw-output '.channel_1_export_offset // 0.0' $CONFIG_PATH)
export CHANNEL_2_IMPORT_OFFSET=$(jq --raw-output '.channel_2_import_offset // 0.0' $CONFIG_PATH)
export CHANNEL_2_EXPORT_OFFSET=$(jq --raw-output '.channel_3_export_offset // 0.0' $CONFIG_PATH)
export CHANNEL_3_IMPORT_OFFSET=$(jq --raw-output '.channel_3_import_offset // 0.0' $CONFIG_PATH)
export CHANNEL_3_EXPORT_OFFSET=$(jq --raw-output '.channel_3_export_offset // 0.0' $CONFIG_PATH)

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
echo "Offsets (pro Kanal):"
echo "  Kanal 1: Import +${CHANNEL_1_IMPORT_OFFSET}, Export +${CHANNEL_1_EXPORT_OFFSET}"
echo "  Kanal 2: Import +${CHANNEL_2_IMPORT_OFFSET}, Export +${CHANNEL_2_EXPORT_OFFSET}"
echo "  Kanal 3: Import +${CHANNEL_3_IMPORT_OFFSET}, Export +${CHANNEL_3_EXPORT_OFFSET}"
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
