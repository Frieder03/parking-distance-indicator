"""Distance measurement with one ultrasonic sensor (TRIG/ECHO type)."""
import statistics
import time

import config
from hardware import GPIO


def _wait_for_level(level, timeout_s):
    """Wait until ECHO has the given level. Return the time, or None on timeout."""
    deadline = time.perf_counter() + timeout_s
    while GPIO.input(config.PIN_ECHO) != level:
        if time.perf_counter() > deadline:
            return None
    return time.perf_counter()


def echo_time_to_cm(echo_time_s):
    """Convert the echo time to a distance. The sound travels there and back."""
    return echo_time_s * config.SPEED_OF_SOUND_CM_S / 2


def read_once():
    """Send one ping. Return the distance in cm, or None if it is not valid."""
    # ECHO must be low before a new measurement starts.
    if _wait_for_level(GPIO.LOW, config.ECHO_TIMEOUT_S) is None:
        return None

    # A 10 microsecond pulse on TRIG starts the measurement.
    GPIO.output(config.PIN_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(config.PIN_TRIG, GPIO.LOW)

    # ECHO stays high for as long as the sound is travelling.
    start = _wait_for_level(GPIO.HIGH, config.ECHO_TIMEOUT_S)
    if start is None:
        return None
    end = _wait_for_level(GPIO.LOW, config.ECHO_TIMEOUT_S)
    if end is None:
        return None

    distance = echo_time_to_cm(end - start)
    if config.MIN_DISTANCE_CM <= distance <= config.MAX_DISTANCE_CM:
        return distance
    return None


def read_distance():
    """Return the median of several pings in cm, or None if most are invalid."""
    readings = []
    for _ in range(config.READINGS_PER_MEASUREMENT):
        distance = read_once()
        if distance is not None:
            readings.append(distance)
        time.sleep(config.PAUSE_BETWEEN_PINGS_S)

    if len(readings) <= config.READINGS_PER_MEASUREMENT // 2:
        return None
    return statistics.median(readings)
