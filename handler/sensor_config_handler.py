import json
import logging


class SensorConfigHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def handle_sensor_config(self, sensor_config):
        logging.info(f"Handle sensor config: {sensor_config}")
        topic = f"sensor/{sensor_config.sensor_id}/config"
        message = json.dumps(sensor_config.config)
        self.mqtt_client.publish(topic, message, retain=True)
        logging.info(f"Published sensor config: [{topic}] - {message}")
