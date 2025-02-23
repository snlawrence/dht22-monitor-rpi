# DHT22 Monitor

Publish temperature and humidity to a MQTT broker using a DHT22 sensor on a Raspberry Pi

## Quick start

### Prerequisites

The following dependencies are required if running locally (ie. not in the docker container).
If you plan to run only in docker, then skip these prerequisites.

`apt-get install libgpiod2`

### Environment

Create a `.env` file in the root directory of the repo with the following keys:

```
MQTT_BROKER=
MQTT_PORT=
MQTT_TOPIC=
SENSOR_NAME=
INTERVAL_SECONDS=300
GPIO_PIN=
```

Notes:

- `MQTT_BROKER`: IP address of the broker (`localhost` if the broker is on the same system).
- `INTERVAL_SECONDS`: the sleep duration in seconds between data read/send (300 seconds being 5 minutes).
- `GPIO_PIN`: the GPIO pin number, not the board pin number (eg. pin 7 is GPIO4 so `GPIO_PIN=4` if the sensor data pin is connected to pin 7)

## Running

Run locally with `uv` using `uv run src/monitor.py`.

Start a detached docker container with `docker-compose up -d`.

## Customising

Change the data payload in the `DH22Monitor.read_and_publish()` function as required.