"""Warning levels and the three LEDs."""
import config
from hardware import GPIO

PINS = {
    "green": config.PIN_LED_GREEN,
    "yellow": config.PIN_LED_YELLOW,
    "red": config.PIN_LED_RED,
}


def warning_level(distance_cm):
    """Return "green", "yellow" or "red", or None without a valid distance."""
    if distance_cm is None:
        return None
    if distance_cm < config.RED_BELOW_CM:
        return "red"
    if distance_cm < config.YELLOW_BELOW_CM:
        return "yellow"
    return "green"


def show(level):
    """Switch on only the LED of this level. None switches all LEDs off."""
    for name, pin in PINS.items():
        GPIO.output(pin, GPIO.HIGH if name == level else GPIO.LOW)
