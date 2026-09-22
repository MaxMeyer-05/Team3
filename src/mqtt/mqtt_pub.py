import paho.mqtt.publish as publish
import json
from datetime import datetime, timezone

BROKER_HOST = "192.168.0.10"
DASHBOARD_TOPIC = "dashboard"

def publish_message(topic: str, message: str, hostname: str = BROKER_HOST):
    """
    Publishes a single MQTT message to the specified topic on the given hostname.   
    Args:
        topic (str): The MQTT topic to publish the message to.
        message (str): The message payload to send.
        hostname (str, optional): The hostname of the MQTT broker. Defaults to "localhost".
    """
    publish.single(topic, message, hostname=hostname, qos=1)


def create_access_message(station_id: int, user_code: int) -> dict:
    """Create a request that asks whether a group may start this station."""
    return {
        "message_type": "access_request",
        "station_id": station_id,
        "user_code": user_code,
    }


def create_start_message(station_id: int, user_code: int) -> dict:
    return {
        "message_type": "station_start",
        "station_id": station_id,
        "user_code": user_code,
        "data": {
            "start_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        },
    }


def create_end_message(station_id: int, user_code: int, feedback: str) -> dict:
    return {
        "message_type": "station_end",
        "station_id": station_id,
        "user_code": user_code,
        "data": {
            "end_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "feedback": feedback,
        },
    }


def request_access(station_id: int, user_code: int):
    """Ask the dashboard whether the group may start the station."""
    publish_message(DASHBOARD_TOPIC, json.dumps(create_access_message(station_id, user_code)))


def station_start(station_id: int, user_code: int):
    """Report that an allowed group has started the station."""
    publish_message(DASHBOARD_TOPIC, json.dumps(create_start_message(station_id, user_code)))


def station_end(station_id: int, user_code: int, feedback: str = ""):
    """Report that a group has completed the station."""
    publish_message(DASHBOARD_TOPIC, json.dumps(create_end_message(station_id, user_code, feedback)))

