"""Switch on all three LEDs until Ctrl+C is pressed, to check the wiring."""
import time

import hardware
from hardware import GPIO


def main():
    hardware.setup()
    try:
        for pin in hardware.LED_PINS:
            GPIO.output(pin, GPIO.HIGH)
        print("All LEDs are on. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        hardware.cleanup()


if __name__ == "__main__":
    main()
