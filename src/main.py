import paho.mqtt.client as mqtt
import mqtt.mqtt_sub as mqtt_sub

BROKER_HOST = "localhost"

client = mqtt.Client()
client.on_connect = mqtt_sub.on_connect
client.on_message = mqtt_sub.on_message
client.connect(BROKER_HOST)
client.loop_forever()
