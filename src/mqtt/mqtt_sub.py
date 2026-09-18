import json

import paho.mqtt.client as mqtt
import service.save_data as save_data

from mqtt.mqtt_pub import publish_message
from service.rw_json import create_access_response, read_message_json, write_user_json

BROKER_HOST = "192.168.0.10"
STATION_TOPIC = "station/0"

def on_message(client, userdata, message):
	"""
	Validates a station request and publishes its access response.
	Args:
		client: The MQTT client instance.
		userdata: The private user data as set in Client() or userdata_set().
		message: The MQTT message instance containing topic and payload.
	"""
	try:
		# Decode the incoming MQTT message payload and parse it as JSON.
		payload = read_message_json(message.payload.decode("utf-8"))

		station_id = int(payload["station_id"])
		user_code = int(payload["user_code"])

        # Generate the access response for the station request.
		access_response = create_access_response(user_code, station_id)
		if access_response["isAllowed"] and "data" in payload:
			if not isinstance(payload["data"], dict):
				raise TypeError("data must be an object")
			save_data.save_data(user_code, station_id, payload["data"])

        # Prepare the response payload for the station.
		response = {
			"is_allowed": access_response["isAllowed"],
			"difficulty": access_response["difficulty"],
		}

        # Publish the response to the station's topic.
		publish_message(
			f"station/{station_id}",
			write_user_json(response),
			hostname=BROKER_HOST,
		)
	except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
		print(f"Invalid station request on {message.topic}: {error}")


def on_connect(client, userdata, flags, reason_code, properties=None):
	"""
	Handles the event when the MQTT client connects to the broker.
	Args:
		client: The MQTT client instance.
		userdata: The private user data as set in Client() or userdata_set().
		flags: Response flags sent by the broker.
		reason_code: The connection result.
		properties: MQTT v5.0 properties.
	"""
	client.subscribe(STATION_TOPIC)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST)
client.loop_forever()
