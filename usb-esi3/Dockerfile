ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

# Python und Abhängigkeiten installieren
RUN apk add --no-cache \
    python3 \
    py3-pip \
    && pip3 install --no-cache-dir --break-system-packages \
    pyserial \
    paho-mqtt

# Arbeitsverzeichnis
WORKDIR /app

# Skripte kopieren
COPY run.sh /app/
COPY usb-esi3.py /app/
COPY requirements.txt /app/

# Ausführbar machen
RUN chmod a+x /app/run.sh

CMD [ "/app/run.sh" ]
```

#### 3.3 `usb-esi3/build.yaml`

```yaml
build_from:
  aarch64: ghcr.io/home-assistant/aarch64-base:3.19
  amd64: ghcr.io/home-assistant/amd64-base:3.19
  armv7: ghcr.io/home-assistant/armv7-base:3.19
  armhf: ghcr.io/home-assistant/armhf-base:3.19
