import paho.mqtt.client as mqtt
from paho.mqtt.client import SubscribeOptions
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
import threading
import sys

# セッション有効期限を30秒に設定。指定時間内に再接続しないとセッション情報が消去される。
properties = Properties(PacketTypes.CONNECT)
properties.SessionExpiryInterval = 30
# V5を使用。セッションを使用するためユニークなクライアントIDを設定する
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "idsub2", protocol=mqtt.MQTTv5)
# メッセージ受信時の処理
client.on_message = lambda client, userdata, message: print(message.payload.decode())
# 接続時にセッション情報の消去を行わない
client.connect("192.168.1.6", clean_start=False, properties=properties)
# セッションを使用するため、qos=1（At least onece）
client.subscribe("test",options=SubscribeOptions(qos=1))

def keyboard_listener():
    input("Press Enter to stop...\n")
    # 切断及びループ停止
    client.disconnect()

listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.start()

# ループ開始
client.loop_forever()
