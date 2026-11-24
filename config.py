"""All settings in one place: pins, thresholds and timing."""

# GPIO pins (BCM numbering)
PIN_LED_GREEN = 17
PIN_LED_YELLOW = 27
PIN_LED_RED = 22
PIN_TRIG = 23
PIN_ECHO = 24

# Warning thresholds in cm
RED_BELOW_CM = 10      # closer than this: red
YELLOW_BELOW_CM = 30   # closer than this: yellow, otherwise green

# Sensor
SPEED_OF_SOUND_CM_S = 34300   # at 20 °C
MIN_DISTANCE_CM = 2           # readings outside this range are invalid
MAX_DISTANCE_CM = 400
ECHO_TIMEOUT_S = 0.05         # give up if the echo takes longer than this
PAUSE_BETWEEN_PINGS_S = 0.06  # lets old echoes fade away
READINGS_PER_MEASUREMENT = 3  # the median of these is used
