from dataclasses import dataclass
from datetime import datetime
from typing import List, Any, Optional, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False



@dataclass
class Alert:
    sender_name: str
    event: str
    start: datetime
    end: datetime
    description: str
    tags: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Alert':
        assert isinstance(obj, dict)
        sender_name = from_str(obj.get("sender_name"))
        event = from_str(obj.get("event"))
        start = datetime.fromtimestamp(from_int(obj.get("start")))
        end = datetime.fromtimestamp(from_int(obj.get("end")))
        description = from_str(obj.get("description"))
        tags = from_list(from_str, obj.get("tags"))
        return Alert(sender_name, event, start, end, description, tags)


@dataclass
class Weather:
    id: int
    main: str
    description: str
    icon: str

    @staticmethod
    def from_dict(obj: Any) -> 'Weather':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        main = from_str(obj.get("main"))
        description = from_str(obj.get("description"))
        icon = from_str(obj.get("icon"))
        return Weather(id, main, description, icon)

@dataclass
class Rain:
    one_hour: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Rain':
        assert isinstance(obj, dict)
        one_hour = from_union([from_float, from_none], obj.get("1h"))
        return Rain(one_hour)

@dataclass
class Snow:
    one_hour: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Snow':
        assert isinstance(obj, dict)
        one_hour = from_union([from_float, from_none], obj.get("1h"))
        return Snow(one_hour)

@dataclass
class Current:
    dt: datetime
    sunrise: datetime
    sunset: datetime
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    clouds: int
    uvi: float
    visibility: int
    wind_speed: float
    wind_deg: int
    weather: List[Weather]
    wind_gust: Optional[float] = None
    rain: Optional[Rain] = None
    snow: Optional[Snow] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Current':
        assert isinstance(obj, dict)
        dt = datetime.fromtimestamp(from_int(obj.get("dt")))
        sunrise = datetime.fromtimestamp(from_int(obj.get("sunrise")))
        sunset = datetime.fromtimestamp(from_int(obj.get("sunset")))
        temp = from_float(obj.get("temp"))
        feels_like = from_float(obj.get("feels_like"))
        pressure = from_int(obj.get("pressure"))
        humidity = from_int(obj.get("humidity"))
        dew_point = from_float(obj.get("dew_point"))
        clouds = from_int(obj.get("clouds"))
        uvi = from_float(obj.get("uvi"))
        visibility = from_int(obj.get("visibility"))
        wind_speed = from_float(obj.get("wind_speed"))
        wind_deg = from_int(obj.get("wind_deg"))
        weather = from_list(Weather.from_dict, obj.get("weather"))
        wind_gust = from_union([from_float, from_none], obj.get("wind_gust"))
        rain = from_union([Rain.from_dict, from_none], obj.get("rain"))
        snow = from_union([Snow.from_dict, from_none], obj.get("snow"))
        return Current(dt, sunrise, sunset, temp, feels_like, pressure, humidity, dew_point, clouds, uvi, visibility, wind_speed, wind_deg, weather, wind_gust, rain, snow)


@dataclass
class FeelsLike:
    day: float
    night: float
    eve: float
    morn: float

    @staticmethod
    def from_dict(obj: Any) -> 'FeelsLike':
        assert isinstance(obj, dict)
        day = from_float(obj.get("day"))
        night = from_float(obj.get("night"))
        eve = from_float(obj.get("eve"))
        morn = from_float(obj.get("morn"))
        return FeelsLike(day, night, eve, morn)


@dataclass
class Temp:
    day: float
    min: float
    max: float
    night: float
    eve: float
    morn: float

    @staticmethod
    def from_dict(obj: Any) -> 'Temp':
        assert isinstance(obj, dict)
        day = from_float(obj.get("day"))
        min = from_float(obj.get("min"))
        max = from_float(obj.get("max"))
        night = from_float(obj.get("night"))
        eve = from_float(obj.get("eve"))
        morn = from_float(obj.get("morn"))
        return Temp(day, min, max, night, eve, morn)


@dataclass
class Daily:
    dt: datetime
    sunrise: datetime
    sunset: datetime
    moonrise: datetime
    moonset: datetime
    moon_phase: float
    temp: Temp
    feels_like: FeelsLike
    pressure: int
    humidity: int
    dew_point: float
    wind_speed: float
    wind_gust: float
    wind_deg: int
    clouds: int
    pop: float
    uvi: float
    weather: List[Weather]
    rain: Optional[float] = None
    snow: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Daily':
        assert isinstance(obj, dict)
        dt = datetime.fromtimestamp(from_int(obj.get("dt")))
        sunrise = datetime.fromtimestamp(from_int(obj.get("sunrise")))
        sunset = datetime.fromtimestamp(from_int(obj.get("sunset")))
        moonrise = datetime.fromtimestamp(from_int(obj.get("moonrise")))
        moonset = datetime.fromtimestamp(from_int(obj.get("moonset")))
        moon_phase = from_float(obj.get("moon_phase"))
        temp = Temp.from_dict(obj.get("temp"))
        feels_like = FeelsLike.from_dict(obj.get("feels_like"))
        pressure = from_int(obj.get("pressure"))
        humidity = from_int(obj.get("humidity"))
        dew_point = from_float(obj.get("dew_point"))
        wind_speed = from_float(obj.get("wind_speed"))
        wind_deg = from_int(obj.get("wind_deg"))
        wind_gust = from_float(obj.get("wind_gust"))
        clouds = from_int(obj.get("clouds"))
        pop = from_float(obj.get("pop"))
        uvi = from_float(obj.get("uvi"))
        weather = from_list(Weather.from_dict, obj.get("weather"))
        rain = from_union([from_float, from_none], obj.get("rain"))
        snow = from_union([from_float, from_none], obj.get("snow"))
        return Daily(dt, sunrise, sunset, moonrise, moonset, moon_phase, temp, feels_like, pressure, humidity, dew_point, wind_speed, wind_gust, wind_deg, clouds, pop, uvi, weather, rain, snow)

@dataclass
class Hourly:
    dt: datetime
    temp: float
    feels_like: float
    pressure: int
    humidity: int
    dew_point: float
    uvi: float
    clouds: int
    visibility: int
    wind_speed: float
    wind_gust: float
    wind_deg: int
    pop: float
    weather: List[Weather]

    @staticmethod
    def from_dict(obj: Any) -> 'Hourly':
        assert isinstance(obj, dict)
        dt = datetime.fromtimestamp(from_int(obj.get("dt")))
        temp = from_float(obj.get("temp"))
        feels_like = from_float(obj.get("feels_like"))
        pressure = from_int(obj.get("pressure"))
        humidity = from_int(obj.get("humidity"))
        dew_point = from_float(obj.get("dew_point"))
        uvi = from_float(obj.get("uvi"))
        clouds = from_int(obj.get("clouds"))
        visibility = from_int(obj.get("visibility"))
        wind_speed = from_float(obj.get("wind_speed"))
        wind_deg = from_int(obj.get("wind_deg"))
        wind_gust = from_float(obj.get("wind_gust"))
        pop = from_float(obj.get("pop"))
        weather = from_list(Weather.from_dict, obj.get("weather"))
        return Hourly(dt, temp, feels_like, pressure, humidity, dew_point, uvi, clouds, visibility, wind_speed, wind_deg, wind_gust, pop, weather)

@dataclass
class Minutely:
    dt: datetime
    precipitation: float

    @staticmethod
    def from_dict(obj: Any) -> 'Minutely':
        assert isinstance(obj, dict)
        dt = datetime.fromtimestamp(from_int(obj.get("dt")))
        precipitation = from_float(obj.get("precipitation"))
        return Minutely(dt, precipitation)


@dataclass
class OpenWeatherData:
    lat: float
    lon: float
    timezone: str
    timezone_offset: int
    current: Current
    minutely: List[Minutely]
    hourly: List[Hourly]
    daily: List[Daily]
    alerts: Optional[List[Alert]]

    @staticmethod
    def from_dict(obj: Any) -> 'OpenWeatherData':
        assert isinstance(obj, dict)
        lat = from_float(obj.get("lat"))
        lon = from_float(obj.get("lon"))
        timezone = from_str(obj.get("timezone"))
        timezone_offset = from_int(obj.get("timezone_offset"))
        current = Current.from_dict(obj.get("current"))
        minutely = from_list(Minutely.from_dict, obj.get("minutely"))
        hourly = from_list(Hourly.from_dict, obj.get("hourly"))
        daily = from_list(Daily.from_dict, obj.get("daily"))
        alerts = alerts = from_union([lambda x: from_list(Alert.from_dict, x), from_none], obj.get("alerts"))
        return OpenWeatherData(lat, lon, timezone, timezone_offset, current, minutely, hourly, daily, alerts)

