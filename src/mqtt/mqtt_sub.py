import paho.mqtt.client as mqtt

def sub_connect(client, topic, hostname: str = "localhost"):
    """
    Connects the given MQTT client to the specified hostname and subscribes to the given topic.
    Args:
        client: The MQTT client instance to connect.
        topic (str): The MQTT topic to subscribe to.
        hostname (str, optional): The hostname of the MQTT broker. Defaults to "localhost".
    """
    client.connect(hostname)
    client.subscribe(topic)

def on_message(client, userdata, message):
    """
    Callback function that is called when a message is received on a subscribed topic.
    Args:
        client: The MQTT client instance.
        userdata: The private user data as set in Client() or userdata_set().
        message: An instance of MQTTMessage, which contains topic, payload, qos, retain.
    """
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message
sub_connect(client, "your/topic")  # Replace "your/topic" with the actual topic you want to subscribe to
client.loop_start()

# Keep the script running to listen for incoming messages
try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
