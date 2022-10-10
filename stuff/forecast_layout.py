from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout


class ForecastLayout(BoxLayout):
    lp = ListProperty()

    def __init__(self, *args, **kwargs):
        super(ForecastLayout, self).__init__(*args, **kwargs)

        l = [0, 100,
             50, 20,
             100, 30,
             150, 10,
             200, 100,
             250, 100,
             300, 16,
             350, 20,
             400, 30,
             450, 35,
             500, 20
             ]
        self.lp = l
        self.bind(lp=self._update)

        i = 5
