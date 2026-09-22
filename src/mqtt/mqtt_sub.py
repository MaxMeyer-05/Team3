import json


def on_connect(client, userdata, flags, reason_code, properties=None):
    """
    Subscribe to the response topic for the configured station.
    Args:
        client: The connected MQTT client instance.
        userdata: The station configuration supplied by main.py.
        flags: MQTT connection flags.
        reason_code: MQTT connection result.
        properties: Optional MQTT v5 properties.
    """
    if reason_code != 0:
        print(f"MQTT connection failed: {reason_code}")
        return

    station_id = userdata["station_id"]
    client.subscribe(f"station/{station_id}")

def on_message(client, userdata, message):
    """
    Callback function that is called when a message is received on a subscribed topic.
    Args:
        client: The MQTT client instance.
        userdata: The private user data as set in Client() or userdata_set().
        message: An instance of MQTTMessage, which contains topic, payload, qos, retain.
    """
    try:
        dashboard_response = json.loads(message.payload.decode("utf-8"))
        print(dashboard_response["is_allowed"])
        print(dashboard_response.get("difficulty"))
    except (json.JSONDecodeError, KeyError, UnicodeDecodeError) as error:
        print(f"Invalid dashboard response on {message.topic}: {error}")
