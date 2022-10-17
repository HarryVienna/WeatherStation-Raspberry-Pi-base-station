from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import paho.mqtt.client as mqtt

class SensorWidget(BoxLayout):

    topic = StringProperty('')
    temperature = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.mqttc = mqtt.Client(client_id="", clean_session=True)
        self.mqttc.on_connect = self.onConnect
        self.mqttc.on_message = self.onMessage
        self.mqttc.connect("localhost", 1883, keepalive=60, bind_address="")
        self.mqttc.loop_start()  # start loop to process callbacks! (new thread!)

    def onConnect(self, client, userdata, flags, rc):
        print("onConnect " + self.topic)
        self.mqttc.subscribe(self.topic, 0)

    def onMessage(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        print ("[INFO   ] [MQTT        ] topic: " + msg.topic +" msg: "+ msg.payload)
        self.temperature = msg.payload