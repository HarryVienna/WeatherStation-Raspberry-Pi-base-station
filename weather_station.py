
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
from kivy.clock import Clock
from open_weather_data import OpenWeatherData
from config import config

from datetime import datetime

class WeatherStation(Widget):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def update(self, dt):
        f = open("tests/json/test6.json", mode="r", encoding="utf-8")

        data = OpenWeatherData.from_dict(json.loads(f.read()))

        print(data);

