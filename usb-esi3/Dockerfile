ARG BUILD_FROM
FROM $BUILD_FROM

# Umgebungsvariablen
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Python und Abhängigkeiten installieren
RUN apk add --no-cache \
    python3 \
    py3-pip \
    jq \
    bash

# Python Pakete installieren
RUN pip3 install --no-cache-dir --break-system-packages \
    pyserial==3.5 \
    paho-mqtt==1.6.1

# Skripte kopieren
COPY run.sh /app/run.sh
COPY usb-esi3.py /app/usb-esi3.py

# Ausführbar machen
RUN chmod +x /app/run.sh

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD pgrep -f usb-esi3.py || exit 1

# Start
CMD ["/app/run.sh"]
