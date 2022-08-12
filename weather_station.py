
import json
import logging
import time
import traceback
from collections import defaultdict
from datetime import datetime
from RPi import GPIO
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from open_weather_data import OpenWeatherData

from datetime import datetime

class WeatherStation(Widget):
    f = open("c:\\Users\\Harald\\NextCloud\\Hardware\\Wetterstation\\Python\\WeatherStation\\test4.json", "r")

    data = OpenWeatherData.from_dict(json.loads(f.read()))

    print(data);
    pass

class WeatherStationApp(App):

    def build(self):
        return WeatherStation()


if __name__ == "__main__":
    WeatherStationApp().run()
