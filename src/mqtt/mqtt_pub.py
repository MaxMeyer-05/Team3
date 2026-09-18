import paho.mqtt.publish as publish
import json
from datetime import datetime, timezone

def publish_message(topic: str, message: str, hostname: str = "localhost"):
    """
    Publishes a single MQTT message to the specified topic on the given hostname.   
    Args:
        topic (str): The MQTT topic to publish the message to.
        message (str): The message payload to send.
        hostname (str, optional): The hostname of the MQTT broker. Defaults to "localhost".
    """
    publish.single(topic, message, hostname=hostname, qos=1)

def create_start_message (station_id, user_code):
    return {
        "station_id": station_id,
        "user_code": user_code, 

        "data":
        {
            "startTime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), #Der aktuelle Timestamp
        }
    }

def create_end_message (station_id, user_code, feedback):
    return {
        "station_id": station_id,
        "user_code": user_code, 
        "data":
        {
            "endTime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), #Der aktuelle Timestamp
            "feedback": feedback
        }
    }

# Bei Station Start:
def Station_Start(station_id = 0, user_code = 00000):
    topic = "station/"+ str(station_id)
    start_message = create_start_message(user_code, station_id)
    #print(start_message)
    publish_message(topic, json.dumps(start_message))

# Bei Station End
def Station_End(station_id = 0, user_code = 00000, feedback = ""):
    topic = "station/"+ str(station_id)
    end_message = create_end_message(user_code, station_id, feedback)
    publish_message(topic, json.dumps(end_message))
