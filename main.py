import asyncio
import logging

import paho.mqtt.client as mqtt

import models
from database import init_database
from handler.sensor_config_handler import SensorConfigHandler
from mqtt import MQTTClient
from setting import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mqtt_client = MQTTClient(
    settings.mqtt_host,
    settings.mqtt_port,
    settings.mqtt_client_id,
    settings.mqtt_username,
    settings.mqtt_password
)

sensor_config_handler = SensorConfigHandler(mqtt_client)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == mqtt.MQTT_ERR_SUCCESS:
        logging.info(f"Connected to MQTT broker {settings.mqtt_host}:{settings.mqtt_port}")
        mqtt_client.subscribe(settings.mqtt_subscriber_topic)
    else:
        logging.info(f"Failed to connect to {settings.mqtt_host}:{settings.mqtt_port} {reason_code}")


def on_message(client, userdata, msg):
    topic = msg.topic
    message = msg.payload.decode('utf-8')
    logging.info(f"Received message from [{topic}] - {message}")
    match topic.split("/")[-1]:
        case "sensor":
            sensor_config_handler.handle_sensor_config(models.SensorConfig.model_validate_json(message))


async def main():
    await init_database()

    mqtt_client.set_on_connect_callback(on_connect)
    mqtt_client.set_on_message_callback(on_message)

    await mqtt_client.connect()

    stop_event = asyncio.Event()

    async def wait_for_stop():
        await stop_event.wait()
        await mqtt_client.disconnect()
        logging.info("MQTT client stopped.")

    stop_task = asyncio.create_task(wait_for_stop())

    try:
        await stop_task
    except asyncio.CancelledError:
        pass


if __name__ == '__main__':
    asyncio.run(main())