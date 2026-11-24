"""Parking distance indicator: one sensor, three LEDs.

Run:             python3 main.py
Without a Pi:    python3 main.py --simulate
Stop:            Ctrl+C
"""
import hardware
import leds
import sensor


def main():
    hardware.setup()
    try:
        while True:
            distance = sensor.read_distance()
            level = leds.warning_level(distance)
            leds.show(level)
            if distance is None:
                print("no valid reading")
            else:
                print(f"{distance:6.1f} cm  {level}")
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        hardware.cleanup()


if __name__ == "__main__":
    main()
