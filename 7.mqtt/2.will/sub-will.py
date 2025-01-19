import paho.mqtt.client as mqtt
import threading
import sys

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client.on_message = lambda client, userdata, message: print(message.payload.decode())
client.connect("192.168.1.6")
client.subscribe("test/will")

def keyboard_listener():
    input("Press Enter to stop...\n")
    client.disconnect()

listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.start()

client.loop_forever()
