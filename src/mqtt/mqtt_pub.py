import paho.mqtt.publish as publish

def publish_message(topic: str, message: str, hostname: str = "localhost"):
    """
    Publishes a single MQTT message to the specified topic on the given hostname.   
    Args:
        topic (str): The MQTT topic to publish the message to.
        message (str): The message payload to send.
        hostname (str, optional): The hostname of the MQTT broker. Defaults to "localhost".
    """
    publish.single(topic, message, hostname=hostname)

    #UserCode, StationID, Optional1, Optional2


{
  "device_id": "sensor-01",
  "timestamp": "2026-09-18T14:32:00Z",
  "data": {
    "temperature": 23.5,
    "humidity": 61
  },
  "status": "ok"
}
g = ("x",3,2)
print(g)
