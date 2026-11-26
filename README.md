# Parking Distance Indicator

Semester project for *Practical IoT with Raspberry Pi*, Universidad Politécnica de Madrid (ETSIDI).

A Raspberry Pi measures the distance to an obstacle with an ultrasonic sensor and
warns with three LEDs (green, yellow, red) and a buzzer that beeps faster as the
obstacle gets closer. Every measurement is sent over **MQTT** to a **Flask** web
dashboard, which shows a car reversing into a parking bay in real time. Warning
thresholds and the buzzer can be changed in the browser through a **REST API**.

```
Pi (main.py) --MQTT--> broker --MQTT--> dashboard.py (Flask) --HTTP/REST--> browser
     ^                                        |
     +------------- MQTT settings <-----------+
```

## Repository structure

| Folder | Content |
|--------|---------|
| [`code/`](code/) | Python program for the Raspberry Pi and the web dashboard. Wiring, installation and usage: [`code/README.md`](code/README.md) |
| [`report/`](report/) | Project report in LaTeX (`main.tex`), figures and the compiled [`main.pdf`](report/main.pdf) |
| [`docs/`](docs/) | Project guidelines of the course and photos of the prototype |

## Quick start on the Raspberry Pi

```bash
git clone https://github.com/Frieder03/parking-distance-indicator.git
cd parking-distance-indicator/code
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install "paho-mqtt>=2" flask
python3 main.py           # terminal 1: sensor, LEDs, buzzer, MQTT
python3 dashboard.py      # terminal 2: web dashboard on http://<ip-of-the-pi>:5001
```

Without a Raspberry Pi: `python3 main.py --simulate`

## Build the report

```bash
cd report
latexmk -pdf main.tex
```

## Team

Felix Secherling, Jarno Henrikus Piter van den Ouden, Frieder Bunne
