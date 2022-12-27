import paho.mqtt.client as mqtt
from kivy.uix.boxlayout import BoxLayout

from config import Config


class SensorWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cfg = Config("config/config.yaml")
        self.mqttc = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)

    def on_kv_post(self, base_widget):
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.connect(self.cfg.params["mqtt"]['mqtt_host'], 1883, keepalive=60, bind_address="")
        self.mqttc.loop_start()  # start loop to process callbacks! (new thread!)

    def on_connect(self, client, userdata, flags, rc):
        print("on_connect " + self.topic)
        self.mqttc.subscribe(self.topic, 0)
