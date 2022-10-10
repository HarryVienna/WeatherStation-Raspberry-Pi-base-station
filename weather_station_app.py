import locale


from kivy.app import App
from kivy.clock import Clock

from kivy.core.window import Window


from open_weather_api import OpenWeatherApi
from config import Config
from weather_station import WeatherStation


class WeatherStationApp(App):

    cfg = Config("config/config.yaml")

    def __init__(self):
        super().__init__()


        self.kv_directory = WeatherStationApp.cfg.params["kivy"]['kv_directory']

    def build(self):
        Window.use_syskeyboard = False
        Window.allow_vkeyboard = True
        Window.single_vkeyboard = True
        Window.docked_vkeyboard = False

        locale.setlocale(locale.LC_TIME, "de_DE")

        weather_station = WeatherStation()
        #weather_station = OpenWeatherApi(self.cfg.getparam("openweather").get("url"))

        Clock.schedule_interval(weather_station.update_weather, 1.0)
        Clock.schedule_interval(weather_station.update_time, 1.0)
        return weather_station


if __name__ == "__main__":
    WeatherStationApp().run()
