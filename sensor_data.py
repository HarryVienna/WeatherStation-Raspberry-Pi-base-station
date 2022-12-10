from dataclasses import dataclass
from typing import Any


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False

def from_none(x: Any) -> Any:
    assert x is None
    return x

@dataclass
class Bme280:
    temperature: float
    humidity: float
    pressure: float

    @staticmethod
    def from_dict(obj: Any) -> 'Bme280':
        _temperature = float(obj.get("temperature"))
        _humidity = float(obj.get("humidity"))
        _pressure = float(obj.get("pressure"))
        return Bme280(_temperature, _humidity, _pressure)

@dataclass
class Hdc1080:
    temperature: float
    humidity: float

    @staticmethod
    def from_dict(obj: Any) -> 'Hdc1080':
        _temperature = float(obj.get("temperature"))
        _humidity = float(obj.get("humidity"))
        return Hdc1080(_temperature, _humidity)


@dataclass
class Sensors:
    hdc1080: Hdc1080
    bme280: Bme280

    @staticmethod
    def from_dict(obj: Any) -> 'Sensors':
        _hdc1080 = from_union([Hdc1080.from_dict, from_none], obj.get("hdc1080"))
        _bme280 = from_union([Bme280.from_dict, from_none], obj.get("bme280"))
        return Sensors(_hdc1080, _bme280)

@dataclass
class SensorData:
    battery: int
    wifi: int
    sensors: Sensors

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _battery = int(obj.get("battery"))
        _wifi = int(obj.get("wifi"))
        _sensors = Sensors.from_dict(obj.get("sensors"))
        return SensorData(_battery, _wifi, _sensors)


