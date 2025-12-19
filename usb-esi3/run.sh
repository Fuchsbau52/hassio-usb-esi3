#!/usr/bin/with-contenv bashio

# Konfiguration aus Home Assistant lesen
export SERIAL_PORT=$(bashio::config 'serial_port')
export BAUDRATE=$(bashio::config 'baudrate')
export MQTT_HOST=$(bashio::config 'mqtt_host')
export MQTT_PORT=$(bashio::config 'mqtt_port')
export MQTT_USER=$(bashio::config 'mqtt_user')
export MQTT_PASS=$(bashio::config 'mqtt_pass')
export DEVICE_NAME=$(bashio::config 'device_name')
export BASE_TOPIC=$(bashio::config 'base_topic')
export LOG_LEVEL=$(bashio::config 'log_level')

# Logging
bashio::log.info "=========================================="
bashio::log.info "USB-ESI3 zu MQTT Add-on wird gestartet..."
bashio::log.info "=========================================="
bashio::log.info "Serieller Port: ${SERIAL_PORT}"
bashio::log.info "Baudrate: ${BAUDRATE}"
bashio::log.info "MQTT Broker: ${MQTT_HOST}:${MQTT_PORT}"
bashio::log.info "MQTT Benutzer: ${MQTT_USER}"
bashio::log.info "Base Topic: ${BASE_TOPIC}"
bashio::log.info "Log Level: ${LOG_LEVEL}"
bashio::log.info "=========================================="

# Prüfe ob USB-Gerät existiert
if [ ! -e "${SERIAL_PORT}" ]; then
    bashio::log.warning "USB-Gerät ${SERIAL_PORT} nicht gefunden!"
    bashio::log.info "Verfügbare Geräte:"
    ls -la /dev/tty* 2>/dev/null || bashio::log.warning "Keine USB-Geräte gefunden"
fi

# Python Skript starten
exec python3 /app/usb-esi3.py
