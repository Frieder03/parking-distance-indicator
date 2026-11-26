"""Step 3: test the buzzer without the sensor. Stop with Ctrl+C.

You should hear: slow beeps that get faster, then a continuous tone, then silence.
"""
import time

import config
import hardware
from buzzer import Buzzer


def main():
    hardware.setup()
    buzzer = Buzzer()
    try:
        print("Beeps get faster (obstacle comes closer)...")
        start, end = config.YELLOW_BELOW_CM - 1, config.RED_BELOW_CM
        for distance in range(start, end - 1, -1):
            buzzer.update(distance, "yellow")
            time.sleep(0.4)
        print("Continuous tone (red zone)...")
        buzzer.update(5, "red")
        time.sleep(1.5)
        print("Silence (green zone).")
        buzzer.update(50, "green")
        time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        buzzer.close()
        hardware.cleanup()


if __name__ == "__main__":
    main()
