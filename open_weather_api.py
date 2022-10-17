import requests
from kivy import Logger

from open_weather_data import OpenWeatherData


class OpenWeatherApi:

    def __init__(self, url, lat, lon, units, lang, apikey):
        super().__init__()

        self.open_weather_url = url.format(lat=lat, lon=lon, units=units, lang=lang, apikey=apikey)

    def getdata(self):
        Logger.info('Calling API')

        try:
            response = requests.get(self.open_weather_url)
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

        return OpenWeatherData.from_dict(response.json())
