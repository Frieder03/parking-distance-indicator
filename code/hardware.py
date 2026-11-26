"""Selects the real GPIO library, or a simulated one with --simulate."""
import sys

import config

SIMULATE = "--simulate" in sys.argv

if SIMULATE:
    import fake_gpio as GPIO
else:
    try:
        import RPi.GPIO as GPIO
    except ImportError:
        sys.exit(
            "RPi.GPIO was not found. On the Raspberry Pi, install it (see README.md).\n"
            "On another computer, add --simulate to run without hardware."
        )

LED_PINS = (config.PIN_LED_GREEN, config.PIN_LED_YELLOW, config.PIN_LED_RED)


def setup():
    """Configure all pins. All outputs start switched off."""
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for pin in LED_PINS:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_TRIG, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(config.PIN_ECHO, GPIO.IN)
    buzzer_off = GPIO.HIGH if config.BUZZER_ACTIVE_LOW else GPIO.LOW
    GPIO.setup(config.PIN_BUZZER, GPIO.OUT, initial=buzzer_off)
    if SIMULATE:
        print("SIMULATION: no real hardware is used.")


def cleanup():
    """Switch off the LEDs and release the pins."""
    for pin in LED_PINS:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()
