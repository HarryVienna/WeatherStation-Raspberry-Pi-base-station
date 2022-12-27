import datetime
import json
import math
from functools import partial

from kivy import Logger
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty

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

    def on_message(self, client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        Logger.info("Message: " + "topic= " + msg.topic + " msg= " + msg.payload)

        data = SensorData.from_dict(json.loads(msg.payload))
        self.battery = f"{data.battery / 1000.0:.1f}" + " " + self.cfg.params["app"]['battery_unit']
        self.wifi = f"{data.wifi:.0f}" + " " + self.cfg.params["app"]['wifi_unit']

        self.temperature = f"{data.sensors.bme280.temperature:.1f}"
        self.temperature_unit = self.cfg.params["app"]['temperature_unit']
        pressure_sea_level = self.calc_sea_level_pressure(
            data.sensors.bme280.pressure,
            data.sensors.bme280.temperature,
            self.cfg.params["app"]['height_above_sealevel'])
        self.pressure = f"{pressure_sea_level:.0f}" + " " + self.cfg.params["app"]['pressure_unit']
        self.humidity = f"{data.sensors.bme280.humidity:.1f}" + " " + self.cfg.params["app"]['humidity_unit']
        self.last_update = f"{datetime.datetime.today():%H:%M}"

        # Opacity can not be changed directly. You would get this error:
        # "Cannot change graphics instruction outside the main Kivy thread"
        Clock.schedule_once(partial(self.update_opacity, 1.0))

    def update_opacity(self, opacity, *args):
        self.opacity = opacity

    @staticmethod
    def calc_sea_level_pressure(pressure, temperature, altitude):
        # https://de.wikipedia.org/wiki/Barometrische_H%C3%B6henformel

        # Konstanten
        g = 9.80665  # Schwerebeschleunigung in m / s^2
        R = 287.05  # Gaskonstante trockener Luft (= R/M)  in m^2/(s²K)
        a = 0.0065  # vertikaler Temperaturgradient
        C_h = 0.12  # Beiwert zur Berücksichtigung der mittleren Dampfdruckänderung K/hPa
        T_0 = 273.15  # Celsius to Kelvin

        if temperature < 9.1:
            E = 5.6402 * (-0.0916 + math.exp(0.06 * temperature))
        else:
            E = 18.2194 * (1.0463 + math.exp(-0.0666 * temperature))

        # Luftdruck auf Meereshöhe berechnen
        p = pressure * math.exp(altitude * g / (R * (temperature + T_0 + C_h * E + a * (altitude / 2))))

        return p
