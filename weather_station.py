import datetime
import json

from kivy.uix.widget import Widget

from open_weather_data import OpenWeatherData




class WeatherStation(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_weather(self, dt):

        print("update data")
        f = open("tests/json/test20.json", mode="r", encoding="utf-8")

        data = OpenWeatherData.from_dict(json.loads(f.read()))

        self.ids.current_widget.weather_data = data
        self.ids.forecast_hourly_widget.weather_data = data
        self.ids.forecast_daily_widget.weather_data = data


    def update_time(self, dt):

        today = datetime.datetime.today()
        self.ids.time_widget.day = f"{today:%a}"
        self.ids.time_widget.date = f"{today:%x}"
        self.ids.time_widget.time = f"{today:%X}"

