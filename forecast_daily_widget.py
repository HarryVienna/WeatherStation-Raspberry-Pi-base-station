import math
from itertools import chain

from kivy.core.text import Label
from kivy.graphics import Color, PushMatrix, PopMatrix, Translate, Line, Rectangle
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from scipy.interpolate import interp1d


class ForecastDailyWidget(Widget):
    weather_data = ObjectProperty()

    max_precipitation = 20

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

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

            self.redraw_clouds()
            self.redraw_legend()
            self.redraw_rain()
            # self.redraw_temperatures_curves()
            self.redraw_temperatures_lines()

            with self.canvas:
                PopMatrix()

    def redraw_legend(self):
        with self.canvas:
            pix_day = self._get_chart_width() / 8

            # Alternating background
            # day_pos = 0
            # for i in range(len(self.weather_data.daily)):
            #     if (i % 2) == 0:
            #         Color(*get_color_from_hex('#FFFFFF'))
            #     else:
            #         Color(*get_color_from_hex('#F0F0F0'))
            #     Rectangle(pos=(day_pos, 1), size=(pix_day, self._get_chart_height()))
            #     day_pos += pix_day

            # Day ticks
            day_pos = pix_day
            Color(*get_color_from_hex('#2E2E2E40'))
            for i in range(len(self.weather_data.daily) - 1):
                Line(points=[day_pos, 0, day_pos, self._get_chart_height()], width=1)
                day_pos += pix_day


            # Day names
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
            for tick in (0, 1, 5, 10, self.max_precipitation):
                label = Label(text=f'{tick} l', font_size=14)
                label.refresh()
                text = label.texture
                Rectangle(size=text.size,
                          pos=(self._get_chart_width() + 5, self._precipitation_to_pixel(tick, 0, self.max_precipitation) - 8),
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

    def redraw_clouds(self):
        with self.canvas:
            pix_day = self._get_chart_width() / 8
            day_pos = 0
            for daily in self.weather_data.daily:
                clouds = 1 - daily.clouds / 100
                # 0-100 -> 40-100
                clouds = 0.8 * clouds + 0.2 if clouds > 0 else 0

                Color(*get_color_from_hex('#FAF02F' + '{0:02x}'.format(round(clouds * 255))))
                Rectangle(pos=(round(day_pos + 3), 1),
                          size=(round(pix_day - 6), self._get_chart_height() - 2)
                          )

                day_pos = day_pos + pix_day
    def redraw_rain(self):
        with self.canvas:
            pix_day = self._get_chart_width() / 8
            day_pos = 0
            for daily in self.weather_data.daily:
                rain = daily.rain
                snow = daily.snow
                clouds = 1 - daily.clouds / 100

                if rain is None:
                    rain = 0
                if rain is not None and rain > self.max_precipitation:
                    rain = self.max_precipitation
                if snow is None:
                    snow = 0
                if snow is not None and snow > self.max_precipitation:
                    snow = self.max_precipitation

                if rain > 0 and snow > 0:
                    Color(*get_color_from_hex('#FFFFFF'))
                    colors = (get_color_from_hex("#EB8DFA"),
                              get_color_from_hex("#96C6F5" ) )
                    texture = Texture.create(size=(1,len(colors)), colorfmt='rgba', bufferfmt='ubyte')
                    buf = bytes([int(v * 255) for v in chain(*colors)])
                    texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')

                    Rectangle(texture=texture, pos=(round(day_pos + 3), 1),
                              size=(round(pix_day - 6), self._precipitation_to_pixel(rain+snow, 0, self.max_precipitation)))
                elif rain > 0:
                    Color(*get_color_from_hex('#FFFFFF'))
                    Rectangle(pos=(round(day_pos + 3), 1),
                              size=(round(pix_day - 6), self._precipitation_to_pixel(rain, 0, self.max_precipitation))
                              )
                    Color(*get_color_from_hex('#96C6F5' + '{0:02x}'.format(round(daily.pop * 255))))
                    Rectangle(pos=(round(day_pos + 3), 1),
                              size=(round(pix_day - 6), self._precipitation_to_pixel(rain, 0, self.max_precipitation))
                              )
                elif snow > 0:
                    Color(*get_color_from_hex('#FFFFFF'))
                    Rectangle(pos=(round(day_pos + 3), 1),
                              size=(round(pix_day - 6), self._precipitation_to_pixel(snow, 0, self.max_precipitation))
                              )
                    Color(*get_color_from_hex('#EB8DFA' + '{0:02x}'.format(round(daily.pop * 255))))
                    Rectangle(pos=(round(day_pos + 3), 1),
                              size=(round(pix_day - 6), self._precipitation_to_pixel(snow, 0, self.max_precipitation))
                              )

                day_pos = day_pos + pix_day

    def redraw_temperatures_lines(self):
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

    def redraw_temperatures_curves(self):
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
            chart_x_values = list(range(0, round(chart_width_reduced) - 1))

            # chart of minimum/maximum temperatures
            x_values = list(range(0, len(temp_min_values)))
            func_temp_min = interp1d(x_values, temp_min_values, kind='quadratic')
            func_temp_max = interp1d(x_values, temp_max_values, kind='quadratic')

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

    def _precipitation_to_pixel(self, value, min_value, max_value):

        value_sqrt = math.sqrt(value)
        min_sqrt = math.sqrt(min_value)
        max_sqrt = math.sqrt(max_value)

        pix = (value_sqrt - min_sqrt) / (max_sqrt - min_sqrt) * self._get_chart_height()
        #pix = (value - min_value) / (max_value - min_value) * self._get_chart_height()
        return round(pix)

    def _get_chart_width(self):
        return self.width - (self.offset_x_left + self.offset_x_right)

    def _get_chart_height(self):
        return self.height - (self.offset_y_bottom + self.offset_y_top)
