import logging

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

import models
from setting import settings

mongo_client = AsyncIOMotorClient(settings.mongo_url)


async def init_database():
    logging.info("Initializing Database")
    await init_beanie(
        database=mongo_client.get_default_database(),
        document_models=[models.SensorConfig]
    )
    logging.info("Database initialized successfully.")
