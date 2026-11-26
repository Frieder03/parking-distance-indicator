"""Step 1: switch on each LED for one second to check the wiring."""
import time

import hardware
import leds


def main():
    hardware.setup()
    try:
        for name, pin in leds.PINS.items():
            print(f"{name} (GPIO{pin})")
            leds.show(name)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        hardware.cleanup()


if __name__ == "__main__":
    main()
