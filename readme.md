# Station MQTT Client

This project provides the MQTT connection between a physical game station and
the Benni dashboard. It deliberately does not contain game logic. Each station
team can use the provided functions after a PIN was entered, when its game
starts, and when the game is completed.

The station asks the dashboard whether the group identified by the PIN is
allowed to use that station. The dashboard tracks progress and sends a response
back to the station's individual MQTT topic.

## Requirements

- Python 3.10 or later
- Network access to the MQTT broker at `192.168.0.10`
- An MQTT broker running on the dashboard computer
- The `paho-mqtt` Python package

Install the dependency with:

```powershell
sudo apt install python3-paho-mqtt
```

## Configuration And Start

Set the physical station number in [src/main.py](src/main.py):

```python
STATION_ID = 1
```

Every physical station must use its own ID. The broker address is also defined
there and in [src/mqtt/mqtt_pub.py](src/mqtt/mqtt_pub.py):

```python
BROKER_HOST = "192.168.0.10"
```

Start the MQTT receiver from the project root:

```powershell
python src/main.py
```

The program stays connected and listens for dashboard responses. Stop it with
`Ctrl+C`.

## Using The Station API

Import the public functions into the station's own program:

```python
from mqtt.mqtt_pub import request_access, station_end, station_start

STATION_ID = 1

def on_pin_entered(pin: int):
		request_access(STATION_ID, pin)


def on_game_started(pin: int):
		station_start(STATION_ID, pin)


def on_game_completed(pin: int):
		station_end(STATION_ID, pin, feedback="good")
```

Call `request_access()` immediately after the ID pad provides a PIN. The
subscriber's `on_message()` function returns `True` or `False` for a valid
dashboard response. Paho MQTT invokes this function asynchronously and ignores
its return value, so each station team must decide how its own application
consumes the response. Then call `station_start()` when the game begins and
`station_end()` after successful completion.

## MQTT Protocol

All station requests are published to the shared `dashboard` topic. The
dashboard sends its answer to `station/<station_id>`, for example `station/1`.
The station subscribes to this response topic when it connects.

### Access Request

```json
{
	"station_id": 1,
	"user_code": 1234
}
```

### Dashboard Response

```json
{
	"is_allowed": true,
	"difficulty": "medium"
}
```

### Start And Completion Messages

```json
{
	"station_id": 1,
	"user_code": 1234,
	"data": {
		"start_time": "2026-09-22 10:00:00"
	}
}
```

```json
{
	"station_id": 1,
	"user_code": 1234,
	"data": {
		"end_time": "2026-09-22 10:05:00",
		"feedback": "Puzzle completed"
	}
}
```

Timestamps are created automatically in UTC by the provided functions. The
optional `feedback` field may be used for a short station result or note.

## Project Structure

```text
src/
	main.py              MQTT client setup and receiver loop
	mqtt/
		mqtt_pub.py        Public API for dashboard requests and game events
		mqtt_sub.py        Dashboard response subscription and handling
```
