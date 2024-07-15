import logging
from typing import Union

import paho.mqtt.client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.subscribeoptions import SubscribeOptions


class MQTTClient:
    def __init__(self, host, port, client_id, username, password):
        self.host = host
        self.port = port
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id
        )
        self.client.username_pw_set(username, password)

    def set_on_connect_callback(self, on_connect_callback):
        self.client.on_connect = on_connect_callback

    def set_on_message_callback(self, on_message_callback):
        self.client.on_message = on_message_callback

    async def connect(self):
        logging.info("Connecting to MQTT broker")
        try:
            self.client.connect(self.host, port=self.port)
            self.client.loop_start()
        except Exception as e:
            logging.error(f"Error connecting to MQTT broker: {e}")
            raise

    def subscribe(
            self,
            topic: str | tuple[str, int] | tuple[str, SubscribeOptions] | list[tuple[str, int]] | list[
                tuple[str, SubscribeOptions]],
            qos: int = 0,
            options: SubscribeOptions | None = None,
            properties: Properties | None = None
    ):
        self.client.subscribe(topic, qos, options, properties)

    def publish(
            self,
            topic: str,
            payload: Union[str, bytes, bytearray, int, float, None] = None,
            qos: int = 0,
            retain: bool = False,
            properties: Properties | None = None
    ):
        logging.info(
            f"Publishing to MQTT broker: topic={topic} payload={payload} qos={qos} retain={retain} properties={properties}")
        try:
            self.client.publish(topic=topic, payload=payload, qos=qos, retain=retain, properties=properties)
            logging.info(f"Message published")
            return True
        except Exception as e:
            logging.error(f"Error publishing to MQTT broker: {e}")
            return False

    async def disconnect(self):
        logging.info("Disconnecting from MQTT broker")
        try:
            self.client.loop_stop()
            self.client.disconnect()
            logging.info("Disconnected from MQTT broker")
        except Exception as e:
            logging.error(f"Error disconnecting from MQTT broker: {e}")
