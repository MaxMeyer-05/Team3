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
    publish.single(topic, message, hostname=hostname)

def create_start_message (user_code):
    return {

        "station_id": 0, #Eure Stationsnummer als Integer 1-5
        "user_code": user_code, 

        "data":
        {
            "startTime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), #Der aktuelle Timestamp
        }
    }

def create_end_message (user_code, feedback):
    return {

        "station_id": 0, #Eure Stationsnummer als Integer 1-5
        "user_code": user_code, 

        "data":
        {
            "endTime": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), #Der aktuelle Timestamp
            "feedback": feedback
        }
    }

{
  "station_id": "int", #1-5
  "user_code": "int", # randomly generated 5 number code

  "data":
  {
    "startTime": "null", #only on start message
    "endTime": "null", #only on end message
    "difficulty": "easy, medium, hard" ,    #only on start message, default = medium
    "feedback": "happy, neutral, unhappy"   #only on end message
  }
}

# Bei Station Start:
topic = "devices/placeholder"
user_code = 11111

start_message = create_start_message(user_code)
publish_message(topic, json.dumps(start_message))

# Bei Station End
feedback = "happy"
end_message = create_end_message(user_code, feedback)

# Debug
#print(json.dumps(start_message))
#print(json.dumps(end_message))