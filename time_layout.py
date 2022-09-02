from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class TimeLayout(BoxLayout):
    day = StringProperty("xx")
    date = StringProperty("xx")
    time = StringProperty("xx")


