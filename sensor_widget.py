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

    topic = StringProperty('')

    name = StringProperty('')
    temperature = StringProperty('????')
    temperature_unit = StringProperty('')
    pressure = StringProperty('????')
    humidity = StringProperty('????')
    battery = StringProperty('')
    wifi = StringProperty('')
    last_update = StringProperty('')


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

    def onMessage(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        Logger.info("Message: " + "topic= " + msg.topic +" msg= "+ msg.payload)

        data = SensorData.from_dict(json.loads(msg.payload))
        self.battery = f"{data.battery/1000.0:.1f}" + " " + self.cfg.params["kivy"]['battery_unit']
        self.wifi = f"{data.wifi:.0f}" + " " + self.cfg.params["kivy"]['wifi_unit']

        self.temperature = f"{data.sensors.bme280.temperature:.1f}"
        self.temperature_unit = self.cfg.params["kivy"]['temperature_unit']
        self.pressure = f"{data.sensors.bme280.pressure:.0f}" + " " + self.cfg.params["kivy"]['pressure_unit']
        self.humidity = f"{data.sensors.bme280.humidity:.1f}" + " " + self.cfg.params["kivy"]['humidity_unit']
        self.last_update = f"{datetime.datetime.today():%H:%M}"

        # Opacity can not be changed directly. You would get this error:
        # "Cannot change graphics instruction outside the main Kivy thread"
        Clock.schedule_once(partial(self.updateOpacity, 1.0))

    def updateOpacity(self, opacity, *args):
        self.opacity = opacity