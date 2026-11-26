"""All settings in one place: pins, thresholds, timing and communication."""
import os

# GPIO pins (BCM numbering)
PIN_LED_GREEN = 17
PIN_LED_YELLOW = 27
PIN_LED_RED = 22
PIN_TRIG = 23
PIN_ECHO = 24
PIN_BUZZER = 19

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

# Communication (MQTT). Override with e.g.  MQTT_BROKER=192.168.1.20 python3 main.py
MQTT_BROKER = os.environ.get("MQTT_BROKER", "test.mosquitto.org")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "1883"))
BASE_TOPIC = os.environ.get("MQTT_BASE_TOPIC", "etsidi/iot/friederbunne/parking")
TOPIC_STATUS = f"{BASE_TOPIC}/status"      # Pi -> dashboard: every measurement (JSON)
TOPIC_SETTINGS = f"{BASE_TOPIC}/settings"  # dashboard -> Pi: thresholds, buzzer (JSON, retained)
TOPIC_ONLINE = f"{BASE_TOPIC}/online"      # "1" while the Pi runs, "0" (last will) when it stops

# Web dashboard
DASHBOARD_PORT = int(os.environ.get("DASHBOARD_PORT", "5001"))  # 5000 is AirPlay on macOS
DEVICE_TIMEOUT_S = 3           # dashboard shows "offline" after this long without data
