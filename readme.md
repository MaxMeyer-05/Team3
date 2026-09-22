# Dashboard

The dashboard service is the central MQTT and database service for the "Benni
befreien" game. It receives requests from game stations, checks a group's game
progress, and determines whether the requested station may be accessed.
Completion times, feedback, and the difficulty level are stored in a MySQL or
MariaDB database. The database therefore provides the foundation for a
dashboard or high-score display.

## Prerequisites

- Python 3.10 or later
- A running MQTT broker, by default on `localhost`
- MySQL 8.x oder MariaDB 10.x
- The Python packages `paho-mqtt` and `mysql-connector-python`

Install the dependencies with:

```powershell
python -m pip install paho-mqtt mysql-connector-python
```

## Setup and Start

1. Start an MQTT broker, for example Mosquitto on `localhost:1883`.
2. Create the database and import the five game stations:

	 ```powershell
	 mysql -u root -p < docs/benni_db.sql
	 ```

3. Update the database credentials in
	[src/database/db_context.py](src/database/db_context.py) for the local
	database. By default, the service expects the `benni_db` database on
	`localhost` with the `root` user.
4. Create at least one game group in the `user` table. The chosen `user_code`
	must be unique.
5. Start the service from the project root:

	 ```powershell
	 python src/main.py
	 ```

The service connects to the broker, subscribes to `station/0`, and continuously
processes incoming station requests.

## Message Protocol

### Station Request

Stations send a JSON request to the `station/0` topic. `station_id` and
`user_code` are required. The optional `data` object stores station data when
access is granted.

```json
{
	"station_id": 2,
	"user_code": 1234,
	"data": {
		"start_time": "2026-09-22 10:00:00",
		"end_time": "2026-09-22 10:05:00",
		"difficulty": "medium",
		"feedback": "Task completed"
	}
}
```

The permitted values for `difficulty` are `easy`, `medium`, and `hard`. For a
station that is not yet completed, omit `end_time` or set it to `null`. The
service maps JSON fields `start_time` and `end_time` to the database columns
`time_start` and `time_end`.

### Service Response

The service publishes the response to `station/<station_id>`, for example
`station/2`:

```json
{
	"is_allowed": true,
	"difficulty": "medium"
}
```

For an unknown access code, an invalid station ID, or a previously unfinished
step, `is_allowed` is `false`. In that case, `difficulty` may be omitted.

## Game Flow and Access Control

- Station 1 is accessible for every known `user_code`.
- Stations 2 through 5 are released only after the previous station has a
  non-null `time_end` value.
- When data for a station is first saved, a record is created in
  `user_station`; later messages update the start time, end time, or feedback.
- A value submitted as `data.difficulty` updates the game group's difficulty.
- The database view `v_spielzeit` aggregates completed stations and each game
  group's start time, end time, and total game time.

## Project Structure

```text
src/
	main.py                 Entry point and MQTT client
	mqtt/
		mqtt_sub.py           Receiving, validation, and access decisions
		mqtt_pub.py           Publishing station responses
	service/
		rw_json.py            JSON processing and access-control logic
		save_data.py          Persisting station data
	database/
		db_context.py         MySQL connection and database queries
	json/                   Example JSON templates
docs/
	benni_db.sql            Database schema, view, and station master data
```