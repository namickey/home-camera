import paho.mqtt.client as mqtt

# V5を使用。セッションを使用するためIDを設定する
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "idpub", protocol=mqtt.MQTTv5)
# セッション情報の消去を行わない
client.connect("192.168.1.6", clean_start=False)
# スレッド開始、ループ開始
client.loop_start()
# セッションを使用するため、qos=1（At least onece）
result = client.publish("test", payload="Hello, MQTT!", qos=1)
result.wait_for_publish()
# 切断及びループ停止、スレッド停止
client.disconnect()
