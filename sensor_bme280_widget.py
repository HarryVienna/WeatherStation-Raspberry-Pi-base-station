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
from sensor_widget import SensorWidget


class SensorBme280Widget(SensorWidget):

    topic = StringProperty('')

    name = StringProperty('')
    temperature = StringProperty('????')
    temperature_unit = StringProperty('')
    pressure = StringProperty('????')
    humidity = StringProperty('????')
    battery = StringProperty('')
    wifi = StringProperty('')
    last_update = StringProperty('')

    opacity = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



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