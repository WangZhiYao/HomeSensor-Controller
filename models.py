from typing import Dict, Any

from beanie import Document, Indexed


class SensorConfig(Document):
    sensor_id: Indexed(str, unique=True)
    config: Dict[str, Any]

    class Settings:
        name = "sensor_config"
