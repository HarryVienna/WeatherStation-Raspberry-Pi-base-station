import datetime
import json

from kivy import Logger
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
                                               self.cfg.params["openweather"]['apikey'])

    def update_weather(self, dt):

        f = open("tests/json/test1.json", mode="r", encoding="utf-8")

        try:
            #data = OpenWeatherData.from_dict(json.loads(f.read()))
            data = self.open_weather_api.getdata()
        except AssertionError as err:
            Logger.info('Error Calling API')
        else:
            self.ids.current_widget.weather_data = data
            self.ids.forecast_hourly_widget.weather_data = data
            self.ids.forecast_daily_widget.weather_data = data

    def update_time(self, dt):
        self.ids.current_widget.time_data = datetime.datetime.today()
