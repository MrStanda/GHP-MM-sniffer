FROM python:3.13-alpine

LABEL org.opencontainers.image.title="ghp-mm2mqtt" \
      org.opencontainers.image.description="Grundig GHP-MM heat pump Modbus sniffer, publishes to MQTT" \
      org.opencontainers.image.licenses="GPL-3.0-only"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ghp-mm2mqtt.py LICENSE ./
# env-driven config instead of the hardcoded ghp_config.py in the repo root
COPY docker/ghp_config.py ./

# dialout (gid 20) matches the serial device group on Debian / Raspberry Pi OS hosts
RUN adduser -D -H -u 1000 -G dialout ghp
USER ghp

ENTRYPOINT ["python", "/app/ghp-mm2mqtt.py"]
