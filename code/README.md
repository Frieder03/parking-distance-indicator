# Parking distance indicator: code

One ultrasonic sensor, three LEDs and a buzzer. The closer the obstacle, the more
urgent the LED: green, yellow, red. All LEDs are off when there is no valid reading.
The buzzer is silent in the green zone, beeps faster and faster in the yellow
zone and sounds continuously in the red zone.

Every measurement is sent over **MQTT**. A **Flask** web dashboard receives it and
shows a car reversing into a parking bay. The browser talks to the dashboard over
a **REST API**, and new settings travel back to the Pi over MQTT.

```
Pi (main.py) --MQTT--> broker --MQTT--> dashboard.py (Flask) --HTTP/REST--> browser
     ^                                        |
     +------------- MQTT settings <-----------+
```

## Wiring

| Part       | GPIO (BCM) | Physical pin |
|------------|-----------:|-------------:|
| Green LED  | 17         | 11           |
| Yellow LED | 27         | 13           |
| Red LED    | 22         | 15           |
| TRIG       | 23         | 16           |
| ECHO       | 24         | 18           |
| Buzzer +   | 19         | 35           |
| Buzzer -   | GND        | 39           |
| Sensor VCC | 5 V        | 2            |
| GND        | GND        | 6            |

- Put a resistor (220 to 330 ohm) in series with each LED.
- **A 5 V sensor such as the HC-SR04 sends 5 V on ECHO, which can damage the Pi.**
  Use a voltage divider: ECHO - 1 kohm - GPIO24 - 2 kohm - GND.
- Buzzer: set `BUZZER_TYPE` in `config.py` to `"active"` (beeps by itself when
  it gets voltage) or `"passive"` (needs a tone). For a 3-pin buzzer module, connect
  VCC to 3V3, GND to GND and I/O to GPIO19. If it beeps when it should be silent,
  set `BUZZER_ACTIVE_LOW = True`.
- Switch off the Pi before you change the wiring.

## Run on the Raspberry Pi

```bash
git clone https://github.com/Frieder03/parking-distance-indicator.git   # only once
cd parking-distance-indicator/code
git pull                  # get the latest version
python3 check_all_leds.py # optional: all LEDs stay on until Ctrl+C
python3 check_leds.py     # step 1: each LED lights up for one second
python3 check_sensor.py   # step 2: distances are printed
python3 check_buzzer.py   # step 3: beeps get faster, then a continuous tone
python3 main.py           # step 4: everything together
```

If `RPi.GPIO` is missing: `sudo apt install python3-rpi.gpio`.
On a Raspberry Pi 5 use `sudo apt install python3-rpi-lgpio` instead.

## Communication and web dashboard

Install once on the Pi (paho-mqtt 2.x is needed, `apt` only has 1.6):

```bash
python3 -m venv --system-site-packages .venv   # keeps access to RPi.GPIO
source .venv/bin/activate
pip install "paho-mqtt>=2" flask
```

Two terminals on the Pi, both with `source .venv/bin/activate`:

```bash
python3 main.py           # terminal 1: sensor, LEDs, buzzer, sends over MQTT
python3 dashboard.py      # terminal 2: web dashboard
```

Open `http://<ip-of-the-pi>:5001` on a laptop or phone in the same network
(`hostname -I` shows the IP). The dashboard can also run on a laptop instead of
the Pi, as long as both reach the same broker.

Watch the raw MQTT messages: `mosquitto_sub -h test.mosquitto.org -t "etsidi/iot/friederbunne/parking/#" -v`

| Topic                | Direction       | Content                                     |
|----------------------|-----------------|---------------------------------------------|
| `.../parking/status`   | Pi -> dashboard | distance, level and settings (JSON)       |
| `.../parking/settings` | dashboard -> Pi | thresholds and buzzer (JSON, retained)    |
| `.../parking/online`   | Pi -> dashboard | `1` while running, `0` as last will       |

REST API of the dashboard:

```bash
curl http://<ip>:5001/api/status
curl -X PUT -H "Content-Type: application/json" -d '{"red_below_cm": 12}' http://<ip>:5001/api/settings
```

If the university network blocks `test.mosquitto.org`, run your own broker on the Pi
(`sudo apt install mosquitto`) and start both programs with `MQTT_BROKER=localhost`.

## Run without a Raspberry Pi

```bash
python3 main.py --simulate   # simulated sensor, still sends over MQTT
python3 main.py --offline    # without MQTT
```

## Files

| File              | Task                                           |
|-------------------|------------------------------------------------|
| `config.py`       | Pins, thresholds, timing, MQTT settings        |
| `hardware.py`     | Pin setup and cleanup, real or simulated GPIO  |
| `sensor.py`       | Distance measurement                           |
| `leds.py`         | Warning levels and LEDs                        |
| `buzzer.py`       | Beep rhythm for the buzzer (background thread) |
| `main.py`         | Main program                                   |
| `mqtt_link.py`    | MQTT on the Pi: sends status, gets settings    |
| `settings.py`     | Checks and applies remote settings             |
| `dashboard.py`    | Flask web dashboard and REST API               |
| `templates/dashboard.html` | Web page with the live parking view   |
| `check_all_leds.py` | All LEDs on until Ctrl+C                     |
| `check_leds.py`   | LED wiring check                               |
| `check_sensor.py` | Sensor check                                   |
| `check_buzzer.py` | Buzzer check                                   |
| `fake_gpio.py`    | Simulated GPIO                                 |
