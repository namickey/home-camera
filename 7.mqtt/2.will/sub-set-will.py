import paho.mqtt.client as mqtt
import threading
import sys

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, protocol=mqtt.MQTTv5)

# Willメッセージを設定する
# このクライアントの接続が意図せず切れた場合、will(遺書)メッセージが送信される
# 別途、will用のトピックのsubscriveが必要
client.will_set("test/will", payload="Goodbye, MQTT!")
client.on_message = lambda client, userdata, message: print(message.payload.decode())
client.connect("192.168.1.6")

# subscribeする側。subscribeできなくなったらwillメッセージが送信される
client.subscribe("test")

def keyboard_listener():
    input("Press Enter to stop...\n")
    # ループ停止、スレッド停止　※loop_startしたスレッドは、loop_stopで停止が可能
    client.loop_stop()
    # disconnectせずに終了すると、willメッセージが送信される
    sys.exit()

listener_thread = threading.Thread(target=keyboard_listener)
listener_thread.start()

# ループ開始　※loop_startしたスレッドは、loop_stopで停止が可能
client.loop_start()
