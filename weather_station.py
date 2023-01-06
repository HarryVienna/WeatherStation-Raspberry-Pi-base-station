import json
from datetime import datetime

from kivy import Logger
from kivy.clock import Clock
from kivy.uix.widget import Widget

from config import Config
from open_weather_api import OpenWeatherApi
from open_weather_data import OpenWeatherData


class WeatherStation(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cfg = Config("config/config.yaml")

        self.open_weather_api = OpenWeatherApi(self.cfg.params["openweather"]['url'],
                                               self.cfg.params["openweather"]['lat'],
                                               self.cfg.params["openweather"]['lon'],
                                               self.cfg.params["openweather"]['units'],
                                               self.cfg.params["openweather"]['lang'],
                                               self.cfg.params["openweather"]['appid'])

        Clock.schedule_once(self.update_weather)

        Clock.schedule_interval(self.update_weather, self.cfg.params["openweather"]['interval'])
        Clock.schedule_interval(self.update_time, 1.0)

    def update_weather(self, dt):
        Logger.info("update_weather: start")

        # -- for debugging --
        #f = open("tests/json/test6.json", mode="r", encoding="utf-8")
        #data = OpenWeatherData.from_dict(json.loads(f.read()))
        # -------------------

        data = self.open_weather_api.getdata()

        if data is not None:
            self.ids.current_widget.weather_data = data
            self.ids.forecast_hourly_widget.weather_data = data
            self.ids.forecast_daily_widget.weather_data = data
            self.ids.alert_widget.weather_data = data
        Logger.info("update_weather: end")

    def update_time(self, dt):
        self.ids.current_widget.time_data = datetime.today()
