"""MQTT link on the Pi: publishes every measurement and receives new settings.

If the broker cannot be reached, the indicator keeps working locally and paho
keeps trying to reconnect in the background.
"""
import json
import time

import paho.mqtt.client as mqtt

import config

if not hasattr(mqtt, "CallbackAPIVersion"):
    raise ImportError("paho-mqtt 2.x is needed (pip install 'paho-mqtt>=2')")


class MqttLink:
    def __init__(self, on_settings):
        """on_settings(data) is called with the decoded JSON of a settings message."""
        self._on_settings = on_settings
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        # Last will: the broker publishes "0" for us if the Pi disappears.
        self.client.will_set(config.TOPIC_ONLINE, "0", qos=1, retain=True)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.connect_async(config.MQTT_BROKER, config.MQTT_PORT, 60)
        self.client.loop_start()
        print(f"MQTT: connecting to {config.MQTT_BROKER}:{config.MQTT_PORT} ...")

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"MQTT: connection failed ({reason_code}), retrying")
            return
        print(f"MQTT: connected, publishing to {config.TOPIC_STATUS}")
        client.publish(config.TOPIC_ONLINE, "1", qos=1, retain=True)
        # Subscribing here renews the subscription after a reconnect.
        client.subscribe(config.TOPIC_SETTINGS, qos=1)

    def _on_message(self, client, userdata, message):
        if not message.payload:   # an empty retained message only deletes old settings
            return
        try:
            data = json.loads(message.payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            print(f"MQTT: ignoring settings message, invalid JSON: {error}")
            return
        self._on_settings(data)

    def publish_status(self, distance_cm, level, current_settings):
        """Send one measurement. Nothing happens while the broker is unreachable."""
        payload = {
            "time": time.time(),
            "distance_cm": None if distance_cm is None else round(distance_cm, 1),
            "level": level,
            **current_settings,
        }
        self.client.publish(config.TOPIC_STATUS, json.dumps(payload), qos=0)

    def close(self):
        """Say goodbye on the online topic and disconnect."""
        if self.client.is_connected():
            info = self.client.publish(config.TOPIC_ONLINE, "0", qos=1, retain=True)
            info.wait_for_publish(timeout=2)
        self.client.disconnect()
        self.client.loop_stop()
