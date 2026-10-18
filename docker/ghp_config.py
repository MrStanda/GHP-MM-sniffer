# Container replacement for upstream ghp_config.py: settings come from environment variables.
import logging
import os

__all__ = [
    "SERIAL_PORT",
    "MQTT_BROKER",
    "MQTT_PORT",
    "MQTT_TOPIC_PREFIX",
    "MQTT_USERNAME",
    "MQTT_PASSWORD",
]

# ghp-mm2mqtt.py imports this module before its own logging.basicConfig(level=ERROR),
# so configuring logging here wins and makes the level adjustable without patching the script.
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "ERROR").upper(),
    format="%(asctime)s %(levelname)s %(message)s",
)

# serial port
SERIAL_PORT = os.environ.get("SERIAL_PORT", "/dev/ttyUSB0")

# MQTT broker settings
MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
MQTT_TOPIC_PREFIX = os.environ.get("MQTT_TOPIC_PREFIX", "GHP")
# unset or empty connects without authentication
MQTT_USERNAME = os.environ.get("MQTT_USERNAME") or None
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD") or None
