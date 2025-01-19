import paho.mqtt.client as mqtt
import threading
import sys

def on_message(client, userdata, message):
    print(message.payload.decode(), message.properties.CorrelationData.decode())
    client.publish(message.properties.ResponseTopic, payload="Received!", properties=message.properties)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client.on_message = on_message
client.connect("192.168.1.6")
client.subscribe("test")

def keyboard_listener():
    input("Press Enter to stop...\n")
    client.disconnect()

listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.start()

client.loop_forever()
