import locale
import logging

from kivy.app import App
from kivy.logger import Logger, ColoredFormatter

from config import Config
from weather_station import WeatherStation


class WeatherStationApp(App):

    def __init__(self):
        super().__init__()

        self.cfg = Config("config/config.yaml")
        self.kv_directory = self.cfg.params["app"]['kv_directory']

        # Add date/time to logging
        logging.Formatter.default_msec_format = '%s.%03d'
        # FileHandler
        Logger.handlers[1].setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        # ConsoleHandler
        Logger.handlers[2].setFormatter(ColoredFormatter('[%(levelname)-18s] %(asctime)s %(message)s'))

    def build(self):
        # Window.use_syskeyboard = False
        # Window.allow_vkeyboard = True
        # Window.single_vkeyboard = True
        # Window.docked_vkeyboard = False

        locale.setlocale(locale.LC_TIME, self.cfg.params["app"]['locale'])

        return WeatherStation()

    def on_start(self):
        print("on_start ")


if __name__ == "__main__":
    WeatherStationApp().run()
