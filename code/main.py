"""Parking distance indicator: one sensor, three LEDs, a buzzer and MQTT.

Run:             python3 main.py
Without a Pi:    python3 main.py --simulate
Without MQTT:    python3 main.py --offline
Stop:            Ctrl+C
"""
import sys

import hardware
import leds
import sensor
import settings
from buzzer import Buzzer


def connect_mqtt(buzzer):
    """Start the MQTT link, or return None if it is switched off or not installed."""
    if "--offline" in sys.argv:
        return None
    try:
        from mqtt_link import MqttLink
    except ImportError as error:
        print(f"Running without MQTT: {error} (see README.md).")
        return None

    def on_settings(data):
        try:
            checked = settings.validate(data)
        except ValueError as error:
            print(f"MQTT: ignoring settings: {error}")
            return
        settings.apply(checked, buzzer)
        print(f"MQTT: new settings {checked}")

    return MqttLink(on_settings)


def main():
    hardware.setup()
    buzzer = Buzzer()
    link = connect_mqtt(buzzer)
    try:
        while True:
            distance = sensor.read_distance()
            level = leds.warning_level(distance)
            leds.show(level)
            buzzer.update(distance, level)
            if link is not None:
                link.publish_status(distance, level, settings.current(buzzer.enabled))
            if distance is None:
                print("no valid reading")
            else:
                print(f"{distance:6.1f} cm  {level}")
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        if link is not None:
            link.close()
        buzzer.close()
        hardware.cleanup()


if __name__ == "__main__":
    main()
