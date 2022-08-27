
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
from weather_station import WeatherStation
from config import config

from datetime import datetime


class WeatherStationApp(App):
    #URL = "https://api.openweathermap.org/data/3.0/onecall?lat=48.214110&lon=16.323219&units=metric&lang=de&appid=abdb6964a969eeceed4f072180f1d3a7"
    URL = "https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units={units}&lang={lang}&appid={apikey}"
    LAT = 48.214110
    LON = 16.323219
    UNITS = "metric"
    LANG = "de"
    APIKEY = "abdb6964a969eeceed4f072180f1d3a7"

    def build(self):
        Window.use_syskeyboard = False
        Window.allow_vkeyboard = True
        Window.single_vkeyboard = True
        Window.docked_vkeyboard = False

        open_weather_url = self.URL.format(lat=self.LAT, lon=self.LON, units=self.UNITS, lang=self.LANG, apikey=self.APIKEY)
        weather_station = WeatherStation(open_weather_url)

        Clock.schedule_interval(weather_station.update, 10.0)
        return weather_station


if __name__ == "__main__":
    WeatherStationApp().run()
