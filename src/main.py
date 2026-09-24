import paho.mqtt.client as mqtt
from mqtt import mqtt_sub


BROKER_HOST = "192.168.0.10"
STATION_ID = 1

if STATION_ID < 1:
    raise ValueError("STATION_ID must be at least 1")


def on_access_response(is_allowed: bool):
    """
    Handle the response from the access control system.
    Args:
        is_allowed (bool): True if access is allowed, False otherwise.
    """
    if is_allowed:
        print("Access allowed")
        # Proceed with starting the station
    else:
        print("Access denied")
        # Handle access denial, e.g., prompt for PIN again or alert the user


client = mqtt.Client()
client.user_data_set(
    {
        "station_id": STATION_ID,
        "access_response_handler": on_access_response,
    }
)
client.on_connect = mqtt_sub.on_connect
client.on_message = mqtt_sub.on_message

client.connect(BROKER_HOST)
try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
finally:
    client.disconnect()