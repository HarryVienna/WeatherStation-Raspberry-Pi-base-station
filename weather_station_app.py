import locale

from kivy.app import App
from kivy.clock import Clock

from kivy.core.window import Window

from config import Config
from weather_station import WeatherStation


class WeatherStationApp(App):

    def __init__(self):
        super().__init__()

        self.cfg = Config("config/config.yaml")
        self.kv_directory = self.cfg.params["kivy"]['kv_directory']

    def build(self):
        Window.use_syskeyboard = False
        Window.allow_vkeyboard = True
        Window.single_vkeyboard = True
        Window.docked_vkeyboard = False

        locale.setlocale(locale.LC_TIME, self.cfg.params["kivy"]['locale'])

        weather_station = WeatherStation()

        Clock.schedule_once(weather_station.update_weather)

        Clock.schedule_interval(weather_station.update_weather, 60.0 * 5)
        Clock.schedule_interval(weather_station.update_time, 1.0)

        return weather_station

if __name__ == "__main__":
    WeatherStationApp().run()
