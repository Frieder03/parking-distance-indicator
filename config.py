"""All settings in one place: pins, thresholds and timing."""

# GPIO pins (BCM numbering)
PIN_LED_GREEN = 17
PIN_LED_YELLOW = 27
PIN_LED_RED = 22
PIN_TRIG = 23
PIN_ECHO = 24
PIN_BUZZER = 18

# Buzzer
BUZZER_TYPE = "active"      # "active": beeps on its own; "passive": needs a tone (PWM)
BUZZER_ACTIVE_LOW = False   # True for buzzer modules that beep when the pin is LOW
BUZZER_FREQUENCY_HZ = 2000  # tone of a passive buzzer
BEEP_LENGTH_S = 0.08        # length of one beep
BEEP_SLOWEST_S = 0.8        # time between beeps at YELLOW_BELOW_CM
BEEP_FASTEST_S = 0.15       # time between beeps just above RED_BELOW_CM

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
