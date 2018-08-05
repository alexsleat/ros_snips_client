import paho.mqtt.client as mqtt

HOST = 'raspberrypi.local'
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(HOST, rc))

    client.subscribe("hermes/hotword/default/detected")
    client.subscribe("hermes/asr/textCaptured")
    client.subscribe('hermes/intent/#')

def on_message(client, userdata, msg):
    print("Message received on topic {0}: {1}"\
        .format(msg.topic, msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(HOST, PORT, 60)
client.loop_forever()
