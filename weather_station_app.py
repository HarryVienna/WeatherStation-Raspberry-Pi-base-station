import locale

from kivy.app import App
from kivy.core.window import Window

from config import Config
from weather_station import WeatherStation


class WeatherStationApp(App):

    def __init__(self):
        super().__init__()

        self.cfg = Config("config/config.yaml")
        self.kv_directory = self.cfg.params["kivy"]['kv_directory']

    def build(self):
        # Window.use_syskeyboard = False
        # Window.allow_vkeyboard = True
        # Window.single_vkeyboard = True
        # Window.docked_vkeyboard = False

        locale.setlocale(locale.LC_TIME, self.cfg.params["kivy"]['locale'])

        return WeatherStation()

    def on_start(self):
        print("on_start ")


if __name__ == "__main__":
    WeatherStationApp().run()
