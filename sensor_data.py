from typing import Any
from dataclasses import dataclass

@dataclass
class SensorData:
    battery: int
    temperature: float
    humidity: float
    pressure: float

    @staticmethod
    def from_dict(obj: Any) -> 'SensorData':
        _battery = int(obj.get("battery"))
        _temperature = float(obj.get("temperature"))
        _humidity = float(obj.get("humidity"))
        _pressure = float(obj.get("pressure"))
        return SensorData(_battery, _temperature, _humidity, _pressure)
