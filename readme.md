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

### Raspberry Pi Time Synchronization

Configure every station Raspberry Pi to use the dashboard network time server.
This ensures that automatically generated start and end timestamps are
consistent across all stations.

```bash
sudo nano /etc/systemd/timesyncd.conf
```

Set the following value below `NTP=`:

```ini
NTP=192.168.0.254
```

Restart the time synchronization service after saving the file:

```bash
sudo systemctl restart systemd-timesyncd.service
```

## Integrating A Station

Add the station-specific startup and game code in [src/main.py](src/main.py).
Keep the existing MQTT setup at the end of that file: it must run while the
station is waiting for dashboard responses.

### 1. Configure The Station Number

Set `STATION_ID` to the physical number of this station. Every call below uses
this same value.

```python
STATION_ID = 1
```

### 2. Request Access After A PIN Is Entered

Import the three public functions near the other imports in the station's game
code:

```python
from mqtt.mqtt_pub import request_access, station_end, station_start
```

Call `request_access()` immediately after the ID pad has supplied a PIN. Save
that PIN in the game code because it is needed again when the game starts and
ends.

```python
def on_pin_entered(pin: int):
    request_access(STATION_ID, pin)
```

### 3. Start The Game Only After Approval

Add the station's game-start code to the `if is_allowed:` branch of
`on_access_response()` in [src/main.py](src/main.py). This callback is called
after every valid dashboard response. Do not start the game before this
callback confirms access.

Call `station_start()` at the exact point at which the approved group begins
the game:

```python
def on_game_started(pin: int):
    station_start(STATION_ID, pin)
```

### 4. Report A Successful Completion

Call `station_end()` once the game has been completed. `feedback` is optional
and can be an empty string when the station does not collect feedback.

```python
def on_game_completed(pin: int):
    station_end(STATION_ID, pin, feedback="happy")
```

Start the MQTT receiver from the project root:

```powershell
python src/main.py
```

The program stays connected and listens for dashboard responses. Stop it with
`Ctrl+C`.

## MQTT Protocol

All station requests are published to the shared `dashboard` topic. The
dashboard sends its answer to `station/<station_id>`, for example `station/1`.
The station subscribes to this response topic when it connects.

### Access Request

```json
{
	"message_type": "access_request",
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
	"message_type": "station_start",
	"station_id": 1,
	"user_code": 1234,
	"data": {
		"start_time": "2026-09-22 10:00:00"
	}
}
```

```json
{
	"message_type": "station_end",
	"station_id": 1,
	"user_code": 1234,
	"data": {
		"end_time": "2026-09-22 10:05:00",
		"feedback": "happy"
	}
}
```

Timestamps are created automatically in UTC by the provided functions. The
optional `feedback` field may be used for a user feedback.

The dashboard must only publish an `is_allowed` response for messages with
`message_type` set to `access_request`. It stores `station_start` and
`station_end` messages without publishing a response.
## Project Structure

```text
src/
	main.py              MQTT client setup and receiver loop
	mqtt/
		mqtt_pub.py        Public API for dashboard requests and game events
		mqtt_sub.py        Dashboard response subscription and handling
```
