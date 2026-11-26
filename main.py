"""Parking distance indicator: one sensor, three LEDs and a buzzer.

Run:             python3 main.py
Without a Pi:    python3 main.py --simulate
Stop:            Ctrl+C
"""
import hardware
import leds
import sensor
from buzzer import Buzzer


def main():
    hardware.setup()
    buzzer = Buzzer()
    try:
        while True:
            distance = sensor.read_distance()
            level = leds.warning_level(distance)
            leds.show(level)
            buzzer.update(distance, level)
            if distance is None:
                print("no valid reading")
            else:
                print(f"{distance:6.1f} cm  {level}")
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        buzzer.close()
        hardware.cleanup()


if __name__ == "__main__":
    main()
