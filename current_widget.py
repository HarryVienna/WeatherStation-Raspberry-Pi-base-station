from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout

from config import Config


class CurrentWidget(BoxLayout):
    weather_data = ObjectProperty()
    time_data = ObjectProperty('')

    icon = StringProperty('')
    time = StringProperty('')
    temperature = StringProperty('')
    temperature_unit = StringProperty('')
    min_temperature = StringProperty('')
    max_temperature = StringProperty('')

    pressure = StringProperty('')
    humidity = StringProperty('')
    wind = StringProperty('')
    wind_deg = NumericProperty(0)
    clouds = StringProperty('')

    sunrise = StringProperty('')
    sunset = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cfg = Config("config/config.yaml")

    def on_time_data(self, instance, value):
        self.time = f"{self.time_data:%a, %x    %X}"

    def on_weather_data(self, instance, value):

        self.icon = f"icons/weather/{self.weather_data.current.weather[0].icon}.png"
        self.temperature = f"{self.weather_data.current.temp:.1f}"
        self.temperature_unit = self.cfg.params["app"]['temperature_unit']
        self.min_temperature = f"{self.weather_data.daily[0].temp.minimum:.1f}"
        self.max_temperature = f"{self.weather_data.daily[0].temp.maximum:.1f}"

        self.pressure = f"{self.weather_data.current.pressure:.0f}" + " " + self.cfg.params["app"]['pressure_unit']
        self.humidity = f"{self.weather_data.current.humidity:.0f}" + " " + self.cfg.params["app"]['humidity_unit']
        self.wind = f"{self.weather_data.current.wind_speed:.1f}" + " " + self.cfg.params["app"]['wind_unit']
        self.wind_deg = self.weather_data.current.wind_deg * (-1)
        self.clouds = f"{self.weather_data.current.clouds:.0f}" + " " + self.cfg.params["app"]['clouds_unit']

        self.sunrise = f"{self.weather_data.current.sunrise:%H:%M}"
        self.sunset = f"{self.weather_data.current.sunset:%H:%M}"
