from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout


class TestLayout(BoxLayout):
    lp = ListProperty()

    def __init__(self, *args, **kwargs):
        super(TestLayout, self).__init__(*args, **kwargs)

        l = [0, 0,
             50, 30,
             100, 50,
             150, 10,
             200, 30,
             250, 20,
             300, 16,
             350, 20,
             400, 30,
             450, 35,
             500, 20
             ]
        self.lp = l
        self.bind(lp=self._update)


    def _update(self, *args):
        i = 5
