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