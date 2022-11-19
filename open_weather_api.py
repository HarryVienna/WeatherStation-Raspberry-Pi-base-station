import requests
from kivy import Logger

from open_weather_data import OpenWeatherData


class OpenWeatherApi:

    def __init__(self, url, lat, lon, units, lang, appid):
        super().__init__()

        self.url = url
        self.lat = lat
        self.lon = lon
        self.units = units
        self.lang = lang
        self.appid = appid

    def getdata(self):
        Logger.info('Calling API')

        try:
            response = requests.get(self.url, params={"lat": self.lat,
                                                      "lon": self.lon,
                                                      "units": self.units,
                                                      "lang": self.lang,
                                                      "appid": self.appid}, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            Logger.info('Error Calling API')
            return None
        except requests.exceptions.ConnectionError:
            Logger.info('Error Calling API')
            return None
        except requests.exceptions.Timeout:
            Logger.info('Error Calling API')
            return None
        except requests.exceptions.RequestException:
            Logger.info('Error Calling API')
            return None

        #Logger.info(response.content)
        weather_data = None
        try:
            weather_data = OpenWeatherData.from_dict(response.json())
        except AssertionError:
            Logger.error('AssertionError', exc_info=True)
            Logger.error(response.json(), exc_info=False)
        Logger.info('Calling API end')
        return weather_data
