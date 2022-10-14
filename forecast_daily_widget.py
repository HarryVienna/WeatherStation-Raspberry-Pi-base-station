import math

from kivy.core.text import Label
from kivy.graphics import Color, PushMatrix, PopMatrix, Translate, Line, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from scipy.interpolate import interp1d


class ForecastDailyWidget(Widget):
    weather_data = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(ForecastDailyWidget, self).__init__(*args, **kwargs)

        self.weather_data = None

        self.offset_x_left = 32
        self.offset_x_right = 33
        self.offset_y_bottom = 35
        self.offset_y_top = 20

    def on_weather_data(self, instance, value):

        self.redraw()

    def redraw(self):

        if self.weather_data:
            self.canvas.clear()

            with self.canvas:
                PushMatrix()
                Translate(self.x + self.offset_x_left, self.y + self.offset_y_bottom)

            self.redraw_legend()
            self.redraw_rain()
            #self.redraw_temperatures()
            self.redraw_temperatures2()

            with self.canvas:
                PopMatrix()

    def redraw_legend(self):
        with self.canvas:
            # Day names
            pix_day = self._get_chart_width() / 8
            day_pos = pix_day / 2 - 8

            Color(*get_color_from_hex('#000000'))
            for daily in self.weather_data.daily:
                weekday = f"{daily.dt:%a}"

                label = Label(text=weekday, font_size=14)
                label.refresh()
                text = label.texture
                Rectangle(size=text.size, pos=(day_pos, -28), texture=text)

                day_pos += pix_day

            # Rain ticks
            Color(*get_color_from_hex('#000000'))
            for tick in (0, 1, 5, 10, 15, 20):
                label = Label(text=f'{tick} l', font_size=14)
                label.refresh()
                text = label.texture
                Rectangle(size=text.size,
                          pos=(self._get_chart_width() + 5, self._rain_to_pixel(tick, 0, 20) - 8),
                          texture=text)

            # Temperature ticks
            min_temp, min_5_temp, max_temp, max_5_temp = self.weather_data.get_daily_temp_min_max()
            ticks = self._get_ticks(min_5_temp, max_5_temp)

            for tick in ticks:
                Color(*get_color_from_hex('#2E2E2E'))
                Line(points=[0, self._temperature_to_pixel(tick, min_5_temp, max_5_temp),
                             self._get_chart_width(), self._temperature_to_pixel(tick, min_5_temp, max_5_temp)],
                     width=1)

                Color(*get_color_from_hex('#000000'))
                label = Label(text=f'{tick}°', font_size=14)
                label.refresh()
                text = label.texture
                Rectangle(size=text.size,
                          pos=(-26, self._temperature_to_pixel(tick, min_5_temp, max_5_temp) - 8),
                          texture=text)

    def redraw_rain(self):
        with self.canvas:
            pix_day = self._get_chart_width() / 8
            day_pos = 0
            for daily in self.weather_data.daily:
                rain = daily.rain
                if rain is not None:
                    Color(*get_color_from_hex('#2FC7C6' + '{0:02x}'.format(int(daily.pop * 255))))
                    Rectangle(pos=(round(day_pos + 3), 0),
                              size=(round(pix_day - 6), self._rain_to_pixel(rain, 0, 20))
                              )
                day_pos = day_pos + pix_day

    def redraw_temperatures2(self):
        with self.canvas:
            min_temp, min_5_temp, max_temp, max_5_temp = self.weather_data.get_daily_temp_min_max()
            pix_day = self._get_chart_width() / 8
            day_pos = 0

            for daily in self.weather_data.daily:
                Color(rgba=get_color_from_hex("#0000F4"))
                Rectangle(pos=(round(day_pos + 3), self._temperature_to_pixel(daily.temp.minimum, min_5_temp, max_5_temp)),
                          size=(round(pix_day - 6), 3))
                # Line(points=[round(day_pos + 3), self._temperature_to_pixel(daily.temp.minimum, min_5_temp, max_5_temp),
                #              round(day_pos + pix_day - 6), self._temperature_to_pixel(daily.temp.minimum, min_5_temp, max_5_temp)],
                #      width=1)

                Color(rgba=get_color_from_hex("#F40000"))
                Rectangle(pos=(round(day_pos + 3), self._temperature_to_pixel(daily.temp.maximum, min_5_temp, max_5_temp)),
                          size=(round(pix_day - 6), 3))
                # Line(points=[round(day_pos + 3), self._temperature_to_pixel(daily.temp.maximum, min_5_temp, max_5_temp),
                #              round(day_pos + pix_day - 6), self._temperature_to_pixel(daily.temp.maximum, min_5_temp, max_5_temp)],
                #      width=1)

                day_pos += pix_day

    def redraw_temperatures(self):
        with self.canvas:
            min_temp, min_5_temp, max_temp, max_5_temp = self.weather_data.get_daily_temp_min_max()
            pix_day = self._get_chart_width() / 8
            # temp_values = []
            temp_min_values = []
            temp_max_values = []
            for daily in self.weather_data.daily:

                # temp_values.append(daily.temp.minimum)
                # temp_values.append(daily.temp.morn)
                # temp_values.append(daily.temp.day)
                # temp_values.append(daily.temp.maximum)
                # temp_values.append(daily.temp.eve)
                # temp_values.append(daily.temp.night)

                temp_min_values.append(daily.temp.minimum)
                temp_max_values.append(daily.temp.maximum)

            # x_values = list(range(0, len(temp_values)))
            # func_temp = interp1d(x_values, temp_values, kind='cubic')
            #
            # for x in list(range(0, self._get_chart_width())):
            #     print (x, x / (self._get_chart_width() - 1), x / (self._get_chart_width() - 1) * (len(temp_values) - 1))
            #     y = func_temp(x / (self._get_chart_width() - 1) * (len(temp_values) - 1))
            #     print (y)
            #     Point(points=(x, self._val_to_pixel(y, min_5_temp, max_5_temp)))

            chart_width_reduced = self._get_chart_width() - pix_day  # chart begins/ends in middle of first and last day
            chart_x_values = list(range(0, int(chart_width_reduced)))

            # chart of minimum/maximum temperatures
            x_values = list(range(0, len(temp_min_values)))
            func_temp_min = interp1d(x_values, temp_min_values, kind='linear')
            func_temp_max = interp1d(x_values, temp_max_values, kind='linear')

            min_points = []
            max_points = []
            for x in chart_x_values:
                y = func_temp_min(x / (chart_width_reduced - 1) * (len(temp_min_values) - 1))
                min_points.append(
                    (x + (pix_day / 2), self._temperature_to_pixel(y, min_5_temp, max_5_temp))
                )

                y = func_temp_max(x / (chart_width_reduced - 1) * (len(temp_max_values) - 1))
                max_points.append(
                    (x + (pix_day / 2), self._temperature_to_pixel(y, min_5_temp, max_5_temp))
                )

            Color(rgba=get_color_from_hex("#0000F4"))
            Line(points=min_points, width=1.1)

            Color(rgba=get_color_from_hex("#F40000"))
            Line(points=max_points, width=1.1)

    def _get_ticks(self, min_value, max_value):

        ticks = list(range(min_value, max_value + 1, 5))  # 5 = Distance between ticks
        return ticks

    def _temperature_to_pixel(self, value, min_value, max_value):

        pix = (value - min_value) / (max_value - min_value) * self._get_chart_height()
        return round(pix)

    def _rain_to_pixel(self, value, min_value, max_value):

        value_sqrt = math.sqrt(value)
        min_sqrt = math.sqrt(min_value)
        max_sqrt = math.sqrt(max_value)

        pix = (value_sqrt - min_sqrt) / (max_sqrt - min_sqrt) * self._get_chart_height()
        return round(pix)

    def _get_chart_width(self):
        return self.width - (self.offset_x_left + self.offset_x_right)

    def _get_chart_height(self):
        return self.height - (self.offset_y_bottom + self.offset_y_top)
