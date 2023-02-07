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
                                                      "appid": self.appid}, verify=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            Logger.error('Error Calling API')
            return None
        except requests.exceptions.ConnectionError:
            Logger.error('Error Calling API')
            return None
        except requests.exceptions.Timeout:
            Logger.error('Error Calling API')
            return None
        except requests.exceptions.RequestException:
            Logger.error('Error Calling API')
            return None

        weather_data = None
        try:
            weather_data = OpenWeatherData.from_dict(response.json())
        except:
            Logger.error('Error reading content %s', response.text, exc_info=False)

        Logger.info('Calling API end')
        return weather_data
