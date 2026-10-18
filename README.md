Since there is no (yet) working modbus connection to Grundig GHP-MM heat pumps with GR-LC07 controller, the only way to get/set parameters is to tap  modbus communication between controller & unit

<img src='images/gr-lc07.jpg' width='200'>

ghp-mm2mqtt.py is quick & dirty hack to publish eavesdropped communication between unit and controller to MQTT (to be consumed by ie HASS)

basic parameters can be set (modbus 0x06 cmd) via MQTT messages to topic GHP/set/slaveid/addr 


4pin SM JST connector: connect your rs485 B to brown and A to red wire (black is GND, orange 12V):

<img src='images/jst-connector.jpg' width='200'> 
<img src='images/modbus2usb.jpg' width='200'>

install & run sniffer:

```
wget https://raw.githubusercontent.com/a1bert01/GHP-MM-sniffer/refs/heads/main/ghp-mm2mqtt.py
#edit to set serial port and mqtt credentials
chmod +x ./ghp-mm2mqtt.py
./ghp-mm2mqtt.py
```

configure mqtt sensors in HASS ![docs/hass-sensors.txt](docs/hass-sensors.txt)

## Docker

Multi-arch image (amd64, arm64, armv7) built by GitHub Actions on every push to `main`:
`ghcr.io/mrstanda/ghp-mm-sniffer:latest`

Needs a Linux host with the RS485 adapter plugged in. Docker Desktop on macOS and Windows
cannot pass USB serial devices into containers.

```
cp .env.example .env    # set broker and credentials
ls /dev/serial/by-id/   # put this path in docker-compose.yml under devices:
docker compose up -d
```

In the image `ghp_config.py` is replaced by [docker/ghp_config.py](docker/ghp_config.py),
which reads environment variables:

| Variable | Default | |
|---|---|---|
| `SERIAL_PORT` | `/dev/ttyUSB0` | serial device inside the container |
| `MQTT_BROKER` | `localhost` | |
| `MQTT_PORT` | `1883` | |
| `MQTT_TOPIC_PREFIX` | `GHP` | |
| `MQTT_USERNAME` | empty | empty means no authentication |
| `MQTT_PASSWORD` | empty | |
| `LOG_LEVEL` | `ERROR` | `INFO` logs every published message |

The container runs as uid 1000 in group `dialout` (gid 20), which matches the serial device
group on Debian and Raspberry Pi OS. If the device has another group on your host, add
`group_add: ["<gid>"]` to the service.
