from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class CurrentWidget(BoxLayout):
    weather_data = ObjectProperty()

    temperature = StringProperty('')
    min_temperature = StringProperty('')
    max_temperature = StringProperty('')

    pressure = StringProperty('')
    humidity = StringProperty('')
    wind = StringProperty('')
    wind_deg = NumericProperty(0)
    clouds = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.weather_data = None

    def on_weather_data(self, instance, value):
        print("CurrentWidget on_weather_data")
        self.temperature = f"{self.weather_data.current.temp:.1f}" + ' °C'
        self.min_temperature = f"{self.weather_data.daily[0].temp.minimum:.1f}" + ' °C'
        self.max_temperature = f"{self.weather_data.daily[0].temp.maximum:.1f}" + ' °C'

        self.pressure = f"{self.weather_data.current.pressure:.0f}" + ' hPa'
        self.humidity = f"{self.weather_data.current.humidity:.0f}" + ' %'
        self.wind = f"{self.weather_data.current.wind_speed:.1f}" + ' m/s'
        self.wind_deg = self.weather_data.current.wind_deg * (-1)
        self.clouds = f"{self.weather_data.current.clouds:.0f}" + ' %'

