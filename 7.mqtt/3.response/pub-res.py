import paho.mqtt.client as mqtt
import threading
import time

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client.on_message = lambda client, userdata, message: print(message.payload.decode(), message.properties.CorrelationData.decode())
client.connect("192.168.1.6")

# 応答用topicをsubscribeし、スレッド開始、ループ開始
client.subscribe("response/topic")
client.loop_start()

def keyboard_listener():
    input("Press Enter to stop...\n")
    client.loop_stop()

listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.start()

properties = mqtt.Properties(mqtt.PacketTypes.PUBLISH)
properties.ResponseTopic = "response/topic"

for i in range(5):
    properties.CorrelationData = bytes("000" + str(i), "utf-8")
    result = client.publish("test", payload="Hello, MQTT!", properties=properties)
    result.wait_for_publish()
    time.sleep(2)
