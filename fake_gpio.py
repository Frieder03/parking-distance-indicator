"""Stand-in for RPi.GPIO so the program also runs without a Raspberry Pi.

It imitates the ultrasonic sensor: an obstacle moves from 60 cm to 4 cm and
back every 20 seconds. Every 25 seconds there is no echo for 3 seconds.
"""
import time

import config

BCM = "BCM"
OUT = "OUT"
IN = "IN"
LOW = 0
HIGH = 1

pin_states = {}
_started = time.perf_counter()
_echo_start = 0.0
_echo_end = 0.0


def _simulated_distance():
    elapsed = time.perf_counter() - _started
    if elapsed % 25 > 22:
        return None
    phase = abs(elapsed % 20 - 10) / 10   # 1 -> 0 -> 1
    return 4 + phase * 56


def setwarnings(_flag):
    pass


def setmode(_mode):
    pass


def setup(pin, _direction, initial=LOW):
    pin_states[pin] = initial


def output(pin, value):
    global _echo_start, _echo_end
    falling = pin_states.get(pin) == HIGH and value == LOW
    pin_states[pin] = value
    if pin == config.PIN_TRIG and falling:
        distance = _simulated_distance()
        if distance is not None:
            _echo_start = time.perf_counter() + 0.0005
            _echo_end = _echo_start + 2 * distance / config.SPEED_OF_SOUND_CM_S


def input(pin):   # same name as in RPi.GPIO
    if pin == config.PIN_ECHO:
        return HIGH if _echo_start <= time.perf_counter() < _echo_end else LOW
    return pin_states.get(pin, LOW)


def cleanup():
    pin_states.clear()


class PWM:
    """Simulated PWM output for a passive buzzer."""

    def __init__(self, pin, frequency_hz):
        self.pin = pin
        self.frequency_hz = frequency_hz
        self.duty_cycle = 0

    def start(self, duty_cycle):
        self.duty_cycle = duty_cycle

    def ChangeDutyCycle(self, duty_cycle):   # same name as in RPi.GPIO
        self.duty_cycle = duty_cycle

    def stop(self):
        self.duty_cycle = 0
