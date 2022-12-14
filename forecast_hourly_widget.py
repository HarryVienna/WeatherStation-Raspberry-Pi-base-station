import math

from kivy.core.text import Label
from kivy.graphics import Color, PushMatrix, PopMatrix, Translate, Line, Rectangle
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from scipy.interpolate import interp1d


class ForecastHourlyWidget(Widget):
    weather_data = ObjectProperty()

    max_precipitation = 5

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

        # self.weather_data = None

        self.offset_x_left = 32
        self.offset_x_right = 26
        self.offset_y_bottom = 35
        self.offset_y_top = 20

        #self.bind(size=self._update, pos=self._update)

    # def _update(self, instance, value):
    #     print("_update")
    #     self.redraw()

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
            self.redraw_temperatures()

            with self.canvas:
                PopMatrix()

    def redraw_legend(self):
        with self.canvas:
            # Rain ticks
            Color(*get_color_from_hex('#000000'))
            for tick in (0, 1, 2, 3, 4, self.max_precipitation):
                label = Label(text=f'{tick} l', font_size=14)
                label.refresh()
                text = label.texture
                Rectangle(size=text.size,
                          pos=(self._get_chart_width() + 5, self.precipitation_to_pixel(tick, 0, self.max_precipitation) - 8),
                          texture=text)

            # Temperature ticks
            min_temp, min_5_temp, max_temp, max_5_temp = self.weather_data.get_hourly_temp_min_max()
            ticks = self._get_ticks(min_5_temp, max_5_temp)
            for tick in ticks:
                Color(*get_color_from_hex('#2E2E2E'))
                Line(points=[0, self._temperature_to_pixel(tick, min_5_temp, max_5_temp), self._get_chart_width(),
                             self._temperature_to_pixel(tick, min_5_temp, max_5_temp)], width=1)

                Color(*get_color_from_hex('#000000'))
                label = Label(text=f'{tick}°', font_size=14)
                label.refresh()
                text = label.texture
                Rectangle(size=text.size,
                          pos=(-26, self._temperature_to_pixel(tick, min_5_temp, max_5_temp) - 8),
                          texture=text)

            # Hour ticks
            pix_hour = self._get_chart_width() / 48
            hour_pos = 0
            Color(*get_color_from_hex('#2E2E2E80'))
            for hourly in self.weather_data.hourly:
                Line(points=[hour_pos, 0, hour_pos, -8], width=1)
                if hourly.dt.hour == 0 and hourly.dt.minute == 0:
                    Line(points=[hour_pos, 0, hour_pos, self._get_chart_height()], width=1)
                hour_pos += pix_hour

            # Hour values
            hour_pos = pix_hour / 2 - 20
            cnt = 0
            Color(*get_color_from_hex('#2E2E2E'))
            for hourly in self.weather_data.hourly:
                if cnt % 12 == 0:
                    hour = f"{hourly.dt:%H:%M}"

                    label = Label(text=hour, font_size=14)
                    label.refresh()
                    text = label.texture
                    Rectangle(size=text.size, pos=(hour_pos, -28), texture=text)

                hour_pos += pix_hour
                cnt += 1

    def redraw_clouds(self):
        with self.canvas:
            pix_hour = self._get_chart_width() / 48
            day_pos = 0
            for hourly in self.weather_data.hourly:
                clouds = 1 - hourly.clouds / 100

                Color(*get_color_from_hex('#FAF02F' + '{0:02x}'.format(round(clouds * 255))))
                Rectangle(pos=(day_pos, 1),
                          size=(pix_hour, self._get_chart_height() - 2)
                          )
                day_pos = day_pos + pix_hour
    def redraw_rain(self):
        with self.canvas:
            pix_hour = self._get_chart_width() / 48
            hour_pos = 0

            for hourly in self.weather_data.hourly:
                pop = hourly.pop
                rain = hourly.rain.one_hour if hourly.rain is not None else 0
                snow = hourly.snow.one_hour if hourly.snow is not None else 0

                if rain > self.max_precipitation:
                    rain = self.max_precipitation

                if snow > self.max_precipitation:
                    snow = self.max_precipitation

                if rain > 0:
                    Color(*get_color_from_hex('#FFFFFF'))
                    Rectangle(pos=(hour_pos, 1),
                              size=(pix_hour - 1, self.precipitation_to_pixel(rain, 0, 5)))
                    Color(*get_color_from_hex('#96C6F5' + '{0:02x}'.format(round(pop * 255))))
                    Rectangle(pos=(hour_pos, 1),
                              size=(pix_hour - 1, self.precipitation_to_pixel(rain, 0, 5)))
                elif snow > 0:
                    Color(*get_color_from_hex('#FFFFFF'))
                    Rectangle(pos=(hour_pos, 1),
                              size=(pix_hour - 1, self.precipitation_to_pixel(snow, 0, 5)))
                    Color(*get_color_from_hex('#EB8DFA' + '{0:02x}'.format(round(pop * 255))))
                    Rectangle(pos=(hour_pos, 1),
                              size=(pix_hour - 1, self.precipitation_to_pixel(snow, 0, 5)))
                elif pop > 0:
                    # There is a probability of precipitation value > 0 but no rain data. Assume 0.025 for visualization
                    Color(*get_color_from_hex('#FFFFFF'))
                    Rectangle(pos=(hour_pos, 1),
                              size=(pix_hour - 1, self.precipitation_to_pixel(0.025, 0, 5)))
                    Color(*get_color_from_hex('#2E61F5' + '{0:02x}'.format(round(pop * 255))))
                    Rectangle(pos=(hour_pos, 1),
                              size=(pix_hour - 1, self.precipitation_to_pixel(0.025, 0, 5)))

                hour_pos = hour_pos + pix_hour

    def redraw_temperatures(self):
        with self.canvas:
            min_temp, min_5_temp, max_temp, max_5_temp = self.weather_data.get_hourly_temp_min_max()

            temp_values = []
            for hourly in self.weather_data.hourly:
                temp_values.append(hourly.temp)

            pix_hour = self._get_chart_width() / 48
            chart_width_reduced = self._get_chart_width() - pix_hour  # chart begins/ends in middle of first and last day
            chart_x_values = list(range(0, round(chart_width_reduced) - 1))

            x_values = list(range(0, len(temp_values)))
            func_temp = interp1d(x_values, temp_values, kind='quadratic')

            points = []
            for x in chart_x_values:
                y = func_temp(x / (chart_width_reduced - 1) * (len(temp_values) - 1))
                points.append(
                    (x + (pix_hour / 2), self._temperature_to_pixel(y, min_5_temp, max_5_temp))
                )

            Color(rgba=get_color_from_hex("#F56101"))
            Line(points=points, width=2)

    def _get_ticks(self, min_value, max_value):

        ticks = list(range(min_value, max_value + 1, 5))  # 5 = Distance between ticks
        return ticks

    def _temperature_to_pixel(self, value, min_value, max_value):

        pix = (value - min_value) / (max_value - min_value) * self._get_chart_height()
        return round(pix)

    def precipitation_to_pixel(self, value, min_value, max_value):

        value_sqrt = math.sqrt(value)
        min_sqrt = math.sqrt(min_value)
        max_sqrt = math.sqrt(max_value)

        pix = (value_sqrt - min_sqrt) / (max_sqrt - min_sqrt) * self._get_chart_height()
        return round(pix)

    def _get_chart_width(self):
        return self.width - (self.offset_x_left + self.offset_x_right)

    def _get_chart_height(self):
        return self.height - (self.offset_y_bottom + self.offset_y_top)
