import datetime

from kivy import Logger
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
import paho.mqtt.client as mqtt
import json

from sensor_data import SensorData


class SensorWidget(BoxLayout):

    topic = StringProperty('')

    name = StringProperty('')
    temperature = StringProperty('')
    pressure = StringProperty('')
    humidity = StringProperty('')
    battery = StringProperty('')
    update = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.mqttc = mqtt.Client(client_id="", protocol=mqtt.MQTTv311)
        self.mqttc.on_connect = self.onConnect
        self.mqttc.on_message = self.onMessage
        self.mqttc.connect("192.168.0.200", 1883, keepalive=60, bind_address="")
        self.mqttc.loop_start()  # start loop to process callbacks! (new thread!)

    def onConnect(self, client, userdata, flags, rc):
        print("onConnect " + self.topic)
        self.mqttc.subscribe(self.topic, 0)

    def onMessage(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        Logger.info("topic: " + msg.topic +" msg: "+ msg.payload)

        data = SensorData.from_dict(json.loads(msg.payload))
        self.update = f"{datetime.datetime.today():%H:%M}"
        self.battery = f"{data.battery:.0f}" + " mV"
