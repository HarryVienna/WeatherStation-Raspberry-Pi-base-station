import datetime

from kivy import Logger
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import paho.mqtt.client as mqtt
import json

from config import Config
from sensor_data import SensorData


class SensorWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cfg = Config("config/config.yaml")

    def on_kv_post(self, base_widget):
        self.mqttc = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
        self.mqttc.on_connect = self.onConnect
        self.mqttc.on_message = self.onMessage
        self.mqttc.connect(self.cfg.params["kivy"]['mqtt_host'], 1883, keepalive=60, bind_address="")
        self.mqttc.loop_start()  # start loop to process callbacks! (new thread!)

    def onConnect(self, client, userdata, flags, rc):
        print("onConnect " + self.topic)
        self.mqttc.subscribe(self.topic, 0)

