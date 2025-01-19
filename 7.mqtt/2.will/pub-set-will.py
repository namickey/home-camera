import paho.mqtt.client as mqtt
import threading
import sys
import time

# MQTT Brokerの設定
broker = "192.168.1.6"
port = 1883
topic = "test/will"
will_message = "I am offline. Goodbye, MQTT!"

def on_connect(client, userdata, flags, rc, properties):
    print(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

# クライアントのインスタンスを作成
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

# `will`メッセージの設定
# このクライアントの接続が意図せず切れた場合、will(遺書)メッセージが送信される
# デフォルトではkeepalive値=60秒毎にping通信が行われていて、
# 別途、will用のトピックのsubscriveが必要
client.will_set(topic, payload=will_message, qos=0, retain=False)

# コールバック関数の設定
client.on_connect = on_connect
client.on_message = on_message
client.on_log = lambda client, userdata, level, buf: print(buf)

# ブローカーへの接続
client.connect(broker, port)
# スレッド開始、ループ開始
client.loop_start()

pub_run_flag = True

def keyboard_listener():
    input("Press Enter to stop...\n")
    client.loop_stop()
    global pub_run_flag
    pub_run_flag = False

listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.start()

while pub_run_flag:
    # 5秒毎にメッセージを送信
    result = client.publish("test", payload="Hello, MQTT!")
    result.wait_for_publish()
    time.sleep(5)
