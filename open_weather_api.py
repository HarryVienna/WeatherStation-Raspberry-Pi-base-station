import urllib.request

from kivy import Logger
from kivy.network.urlrequest import UrlRequest

from open_weather_data import OpenWeatherData


class OpenWeatherApi:

    def __init__(self, url, lat, lon, units, lang, apikey):
        super().__init__()

        self.open_weather_url = url.format(lat=lat, lon=lon, units=units, lang=lang, apikey=apikey)

    def getdata(self):
        Logger.info('Calling API')

        req = UrlRequest(self.open_weather_url)

        req.wait()

        return OpenWeatherData.from_dict(req.result)

