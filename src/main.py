import os

import paho.mqtt.client as mqtt

from mqtt import mqtt_sub


BROKER_HOST = "192.168.0.10"
STATION_ID = 1

if STATION_ID < 1:
    raise ValueError("STATION_ID must be at least 1")

client = mqtt.Client()
client.user_data_set({"station_id": STATION_ID})
client.on_connect = mqtt_sub.on_connect
client.on_message = mqtt_sub.on_message

client.connect(BROKER_HOST)
try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
finally:
    client.disconnect()