import paho.mqtt.client as mqtt_client
from time import sleep

class mqtt(object):

    def __init__(self, host, port, username="", password="", topic=""):

        self.is_connected = False
        self.is_subscribed = False
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client_id = "teste-mqtt-client-as-class"
        self.topic = topic
        self.client = mqtt_client.Client(self.client_id, True)

    def on_connect(self, client, userdata, flags, rc):

        print("Connection returned result: " + str(rc))

        if rc == 0:
            self.is_connected = True
        if self.is_subscribed:
            self.subscribe(self.topic)

    def on_disconnect(self, client, userdata, rc):

        print("Disconnecting reason  " + str(rc))

        self.is_connected = False

    def on_subscribe(self, client, userdata, mid, granted_pos):

        print("Subscribe event start")

        self.is_subscribed = True

    def on_unsubscribe(self, client, userdata, mid, granted_pos):

        print("Unsubscribe envent start")

    def on_message(self, client, userdata, msg):

        received_msg = str(msg.payload)

        print("[MSG RECEBIDA] Topico: " + msg.topic + " / Mensagem: " + received_msg)

    def set_callbacks(self):

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_message = self.on_message

    def connect(self, keepalive=10):

        # self.client.on_connect = self.on_connect
        # self.client.on_disconnect = self.on_disconnect
        # self.client.on_subscribe = self.on_subscribe
        # self.client.on_unsubscribe = self.on_unsubscribe
        # self.client.on_message = self.on_message
        try:
            self.set_callbacks()
            self.client.connect(self.host, self.port, keepalive)
            # self.client.loop_forever()
            self.client.loop_start()
        except Exception as e:
            self.disconnect()
            print("-> Connect Exception <-")

    def disconnect(self):

        try:
            if self.is_connected:
                self.client.disconnect()
                sleep(0.5)
                self.is_connected = False
        except Exception as e:
            self.disconnect()
            print("-> Disconnect Exception <-")

    def reconnect(self):

        try:
            if not self.is_connected:
                self.client.reconnect()
        except Exception as e:
            self.disconnect()
            print("-> Reconnect Exception <-")

    def publish(self, topic, payload):

        try:
            if self.is_connected:
                self.client.publish(topic, payload, qos=1)
            else:
                self.reconnect()
                self.publish(payload)
        except Exception as e:
            self.disconnect()
            print("-> Publish Exception <-")

    def subscribe(self, topic):

        self.topic = topic
        try:
            if self.is_connected:
                self.client.subscribe(topic, qos=1)
                # self.disconnect()
            else:
                self.reconnect()
                self.subscribe(topic)
        except Exception as e:
            self.disconnect()
            print("-> Subscribe Exception <-")

var_mqtt = mqtt("10.0.0.66", 1883)
var_mqtt.connect()
# var_mqtt.publish("Teste de publish")
var_mqtt.subscribe("#")
var_mqtt.publish("teste/inventory", "Teste de pubslish!!!")
sleep(60)
# var_mqtt = mqtt.connect(mqtt, mqtt.host, mqtt.port, 10)

# Informações uteis:
#                   link problema resubscribe:      https://stackoverflow.com/questions/57395474/mqtt-doesnt-send-data-to-subscriber-after-reconnection
#                   outro link:                     https://stackoverflow.com/questions/36429609/mqtt-paho-python-reliable-reconnect


