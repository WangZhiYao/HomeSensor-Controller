import json
import logging


class SunriseSunsetEventHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client

    def handle_sunrise(self, sensor_id):
        self._handle_event(sensor_id, True)

    def handle_sunset(self, sensor_id):
        self._handle_event(sensor_id, False)

    def _handle_event(self, sensor_id, is_sunrise):
        logging.info(f"Handle sunrise sunset: {sensor_id}")
        topic = f"sensor/{sensor_id}/config"
        message = {'collect_illuminance': is_sunrise}
        self.mqtt_client.publish(topic, json.dumps(message), retain=True)
        logging.info(f"Published sensor config: [{topic}] - {message}")
