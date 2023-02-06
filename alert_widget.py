from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex


class AlertWidget(ScrollView):
    weather_data = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__()

        self.label = Label(font_size=16, color=get_color_from_hex('#2E2E2E'))
        self.add_widget(self.label)
        self.bind(pos=self.update_text_position)
        self.bind(size=self.update_text_position)

        #Clock.schedule_interval(self.update_text_position, 1 / 10)

    def on_weather_data(self, instance, value):
        alerts_list = []
        alerts = self.weather_data.alerts
        if alerts is not None:
            for alert in self.weather_data.alerts:
                alerts_list.append(alert.event + ": " + alert.description)
            self.label.text = ' '.join(alerts_list)
        else:
            self.label.text = ""

    def update_text_position(self, *args):
        self.label.x -= 1

        if self.label.x < -(self.width / 2 + self.label.texture_size[0] / 2):
            self.label.x = self.width / 2 + self.label.texture_size[0] / 2
