"""Step 2: print single sensor readings, without the LEDs. Stop with Ctrl+C."""
import time

import hardware
import sensor


def main():
    hardware.setup()
    try:
        while True:
            distance = sensor.read_once()
            print("no valid reading" if distance is None else f"{distance:6.1f} cm")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        hardware.cleanup()


if __name__ == "__main__":
    main()
