import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)
client.connect("192.168.1.6")
client.loop_start()
result = client.publish("test/will", payload="Hello, MQTT!")
result.wait_for_publish()
client.disconnect()
