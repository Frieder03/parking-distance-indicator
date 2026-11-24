# Parking distance indicator: code

One ultrasonic sensor and three LEDs. The closer the obstacle, the more urgent
the LED: green, yellow, red. All LEDs are off when there is no valid reading.

## Wiring

| Part       | GPIO (BCM) | Physical pin |
|------------|-----------:|-------------:|
| Green LED  | 17         | 11           |
| Yellow LED | 27         | 13           |
| Red LED    | 22         | 15           |
| TRIG       | 23         | 16           |
| ECHO       | 24         | 18           |
| Sensor VCC | 5 V        | 2            |
| GND        | GND        | 6            |

- Put a resistor (220 to 330 ohm) in series with each LED.
- **A 5 V sensor such as the HC-SR04 sends 5 V on ECHO, which can damage the Pi.**
  Use a voltage divider: ECHO - 1 kohm - GPIO24 - 2 kohm - GND.
- Switch off the Pi before you change the wiring.

## Run on the Raspberry Pi

```bash
git clone https://github.com/Frieder03/parking-distance-indicator.git   # only once
cd parking-distance-indicator
git pull                  # get the latest version
python3 check_leds.py     # step 1: each LED lights up for one second
python3 check_sensor.py   # step 2: distances are printed
python3 main.py           # step 3: everything together
```

If `RPi.GPIO` is missing: `sudo apt install python3-rpi.gpio`.
On a Raspberry Pi 5 use `sudo apt install python3-rpi-lgpio` instead.

## Run without a Raspberry Pi

```bash
python3 main.py --simulate
```

## Files

| File              | Task                                           |
|-------------------|------------------------------------------------|
| `config.py`       | Pins, thresholds, timing                       |
| `hardware.py`     | Pin setup and cleanup, real or simulated GPIO  |
| `sensor.py`       | Distance measurement                           |
| `leds.py`         | Warning levels and LEDs                        |
| `main.py`         | Main program                                   |
| `check_leds.py`   | LED wiring check                               |
| `check_sensor.py` | Sensor check                                   |
| `fake_gpio.py`    | Simulated GPIO                                 |
