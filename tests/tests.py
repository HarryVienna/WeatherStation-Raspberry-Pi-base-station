import unittest
import json
from open_weather_data import OpenWeatherData

class Testing(unittest.TestCase):

    def runTest(self):
        f = open("json/test16.json", mode="r", encoding="utf-8")
        data = OpenWeatherData.from_dict(json.loads(f.read()))

        self.assertEqual(data.timezone, "Europe/Vienna")

if __name__ == '__main__':
    unittest.main()