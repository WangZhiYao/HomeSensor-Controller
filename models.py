from enum import StrEnum
from typing import Dict, Any

from beanie import Document, Indexed
from pydantic import BaseModel


class SensorConfig(Document):
    sensor_id: Indexed(str, unique=True)
    config: Dict[str, Any]

    class Settings:
        name = "sensor_config"


class EventType(StrEnum):
    SUNRISE = 'sunrise'
    SUNSET = 'sunset'


class Event(BaseModel):
    type: EventType
    sensor_id: str
    timestamp: int
