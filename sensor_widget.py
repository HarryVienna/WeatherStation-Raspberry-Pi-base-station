import datetime

from kivy import Logger
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import paho.mqtt.client as mqtt
import json

from config import Config
from sensor_data import SensorData


class SensorWidget(BoxLayout):

    topic = StringProperty('')

    name = StringProperty('')
    temperature = StringProperty('')
    temperature_unit = StringProperty('')
    pressure = StringProperty('')
    humidity = StringProperty('')
    battery = StringProperty('')
    update = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cfg = Config("config/config.yaml")

        self.mqttc = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
        self.mqttc.on_connect = self.onConnect
        self.mqttc.on_message = self.onMessage
        self.mqttc.connect(self.cfg.params["kivy"]['mqtt_host'], 1883, keepalive=60, bind_address="")
        self.mqttc.loop_start()

    def onConnect(self, client, userdata, flags, rc):
        print("onConnect " + self.topic)
        self.mqttc.subscribe(self.topic, 0)

    def onMessage(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        Logger.info("Message: " + "topic= " + msg.topic +" msg= "+ msg.payload)

        data = SensorData.from_dict(json.loads(msg.payload))

        self.temperature = f"{data.temperature:.1f}"
        self.temperature_unit = self.cfg.params["kivy"]['temperature_unit']
        self.pressure = f"{data.pressure:.1f}" + " " + self.cfg.params["kivy"]['pressure_unit']
        self.humidity = f"{data.humidity:.1f}" + " " + self.cfg.params["kivy"]['humidity_unit']
        self.battery = f"{data.battery:.0f}" + " " + " " + self.cfg.params["kivy"]['battery_unit']
        self.update = f"{datetime.datetime.today():%H:%M}"
