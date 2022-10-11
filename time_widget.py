from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class TimeWidget(BoxLayout):
    date = StringProperty("xx")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


