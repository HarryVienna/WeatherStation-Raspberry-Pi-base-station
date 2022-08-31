import urllib.request
from open_weather_data import OpenWeatherData


class OpenWeatherApi:

    def __init__(self, url, lat, lon, units, lang, apikey):
        super().__init__()

        self.open_weather_url = url.format(lat=lat, lon=lon, units=units, lang=lang, apikey=apikey)

    def getdata(self):
        request = urllib.request.urlopen(self.open_weather_url)

        json = request.read().decode("utf8")

        return OpenWeatherData.from_dict(json.loads(json))

