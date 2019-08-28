import paho.mqtt.client as mqtt_client
from time import sleep


class Mqtt(object):

    def __init__(self, host, port, username="", password="", topic=""):

        self.is_connected = False
        self.is_subscribed = False
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client_id = "teste-mqtt-client-as-class"
        self.topic = topic
        self.subscribed_topics_array = []

    def connect(self, keepalive=10):

        try:
            self.client = mqtt_client.Client(self.client_id, True)
            self.set_callbacks()
            sleep(0.2)

            if not self.is_connected:
                self.client.connect(self.host, self.port, keepalive)
                self.client.loop_start()
                sleep(0.2)

        except Exception as e:
            if self.is_connected:
                self.disconnect()
            print("-> Connect Exception <-")

    def disconnect(self):

        try:
            if self.is_connected:
                self.client.disconnect()
                sleep(0.2)      # era sleep(0.5)
                self.is_connected = False
        except Exception as e:
            self.disconnect()
            print("-> Disconnect Exception <-")

    #Não está sendo utilizado, o propio modulo paho.mqtt.client (biblioteca) está tratando a reconexão
    def reconnect(self, keepalive=10):

        try:
            if not self.is_connected:
                self.connect()
                sleep(0.2)

            if self.subscribed_topics_array:
                if self.is_connected:
                    for topic in self.subscribed_topics_array:
                        self.subscribe(topic)
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

    def subscribe(self, topic="#"):

        self.topic = topic
        try:
            if self.is_connected:
                self.client.subscribe(topic, qos=1)

            else:
                self.connect()
                sleep(0.2)
                self.subscribe(topic)
                sleep(0.2)
                if self.is_subscribed:
                    self.subscribed_topics_array.append(topic)
        except Exception as e:
            self.disconnect()
            print("-> Subscribe Exception <-")

    def set_callbacks(self):

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):

        print("Connection returned result: " + str(rc))

        if rc == 0:
            self.is_connected = True

    def on_disconnect(self, client, userdata, rc):

        print("Disconnecting reason  " + str(rc))

        self.client.loop_stop()
        self.is_connected = False
        self.is_subscribed = False

    def on_subscribe(self, client, userdata, mid, granted_pos):

        print("Subscribe event start")

        self.is_subscribed = True

    def on_unsubscribe(self, client, userdata, mid, granted_pos):

        print("Unsubscribe envent start")

        self.is_subscribed = False

    def on_publish(self, client, userdata, mid):

        print("Data published, mid: " + mid)

    def on_message(self, client, userdata, msg):

        received_msg = str(msg.payload)

        print("[MSG RECEBIDA]/Topico: " + msg.topic)
        print("Mensagem: " + received_msg)
        print("Mensagem: " + received_msg)

var_mqtt = Mqtt("10.0.0.66", 1883, "Teste_Eduardo")

while True:
    if not var_mqtt.is_connected:
        var_mqtt.connect()
        sleep(0.2)
        if var_mqtt.is_connected:
            var_mqtt.subscribe("#")
            sleep(0.2)

'''Informações uteis:
link problema resubscribe: https://stackoverflow.com/questions/57395474/mqtt-doesnt-send-data-to-subscriber-after-reconnection
outro link: https://stackoverflow.com/questions/36429609/mqtt-paho-python-reliable-reconnect'''