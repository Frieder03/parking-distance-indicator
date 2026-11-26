"""Buzzer: silent when far away, beeps faster when closer, continuous when red.

The beeping runs in a background thread, so its rhythm stays steady while the
main loop is busy measuring.
"""
import threading
import time

import config
from hardware import GPIO

_POLL_S = 0.01
_PASSIVE = config.BUZZER_TYPE == "passive"
_ON = GPIO.LOW if config.BUZZER_ACTIVE_LOW else GPIO.HIGH
_OFF = GPIO.HIGH if config.BUZZER_ACTIVE_LOW else GPIO.LOW
_OFF_DUTY = 100 if config.BUZZER_ACTIVE_LOW else 0


def beep_interval(distance_cm, level):
    """Seconds between beeps, 0 for a continuous tone, None for silence."""
    if level == "red":
        return 0
    if level != "yellow":
        return None
    span = config.YELLOW_BELOW_CM - config.RED_BELOW_CM
    fraction = min(max((distance_cm - config.RED_BELOW_CM) / span, 0), 1)
    return config.BEEP_FASTEST_S + fraction * (config.BEEP_SLOWEST_S - config.BEEP_FASTEST_S)


class Buzzer:
    def __init__(self):
        self.enabled = True     # can be switched off, e.g. later from the web interface
        self._interval = None
        self._stop = threading.Event()
        self._pwm = None
        if _PASSIVE:
            self._pwm = GPIO.PWM(config.PIN_BUZZER, config.BUZZER_FREQUENCY_HZ)
            self._pwm.start(_OFF_DUTY)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def update(self, distance_cm, level):
        """Set the beep rhythm for the latest measurement."""
        self._interval = beep_interval(distance_cm, level) if self.enabled else None

    def close(self):
        """Stop the background thread and silence the buzzer."""
        self._stop.set()
        self._thread.join()
        self._sound(False)
        if self._pwm is not None:
            self._pwm.stop()

    def _sound(self, on):
        if self._pwm is not None:
            self._pwm.ChangeDutyCycle(50 if on else _OFF_DUTY)
        else:
            GPIO.output(config.PIN_BUZZER, _ON if on else _OFF)

    def _run(self):
        while not self._stop.is_set():
            interval = self._interval
            if interval is None:
                self._sound(False)
                self._stop.wait(_POLL_S)
                continue
            if interval == 0:
                self._sound(True)
                self._stop.wait(_POLL_S)
                continue

            # One beep, then a pause. The pause ends early if the obstacle
            # comes closer, so the rhythm reacts at once.
            started = time.monotonic()
            self._sound(True)
            self._stop.wait(config.BEEP_LENGTH_S)
            self._sound(False)
            while not self._stop.is_set():
                interval = self._interval
                if not interval or time.monotonic() - started >= interval:
                    break
                self._stop.wait(_POLL_S)
