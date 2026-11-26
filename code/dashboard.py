"""Web dashboard: receives the measurements over MQTT and shows them in the browser.

It runs on the Pi or on any laptop that can reach the MQTT broker.

Run:   python3 dashboard.py
Open:  http://<ip-of-this-computer>:5001

REST API
  GET /api/status     latest measurement and whether the Pi is online
  GET /api/settings   active thresholds and buzzer state
  PUT /api/settings   change them, e.g. {"red_below_cm": 12}
"""
import json
import threading
import time

import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template, request

import config
import settings

app = Flask(__name__)

_lock = threading.Lock()
_state = {"status": None, "received": 0.0, "online": False}


# ---------- MQTT ----------

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT: connection failed ({reason_code}), retrying")
        return
    print(f"MQTT: connected to {config.MQTT_BROKER}, listening on {config.BASE_TOPIC}/#")
    client.subscribe(config.TOPIC_STATUS)
    client.subscribe(config.TOPIC_ONLINE)


def on_message(client, userdata, message):
    text = message.payload.decode("utf-8", errors="replace")
    with _lock:
        if message.topic == config.TOPIC_ONLINE:
            _state["online"] = text == "1"
            return
        try:
            _state["status"] = json.loads(text)
        except json.JSONDecodeError:
            print(f"MQTT: ignoring invalid status message: {text!r}")
            return
        _state["received"] = time.time()
        _state["online"] = True


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


# ---------- REST API ----------

def _snapshot():
    with _lock:
        status = dict(_state["status"] or {})
        age = time.time() - _state["received"]
        online = _state["online"] and age < config.DEVICE_TIMEOUT_S
    return status, online


def _active_settings(status):
    """Settings the Pi reported last, or the defaults before the first message."""
    active = settings.current()
    active.update({key: status[key] for key in settings.FIELDS if key in status})
    return active


@app.get("/")
def index():
    return render_template(
        "dashboard.html",
        broker=config.MQTT_BROKER,
        topic=config.BASE_TOPIC,
        poll_ms=250,
    )


@app.get("/api/status")
def get_status():
    status, online = _snapshot()
    return jsonify({
        "device_online": online,
        "broker_connected": mqtt_client.is_connected(),
        "distance_cm": status.get("distance_cm") if online else None,
        "level": status.get("level") if online else None,
        "settings": _active_settings(status),
    })


@app.get("/api/settings")
def get_settings():
    status, _ = _snapshot()
    return jsonify(_active_settings(status))


@app.put("/api/settings")
def put_settings():
    changes = request.get_json(silent=True)
    if not isinstance(changes, dict):
        return jsonify({"error": "send a JSON object"}), 400
    status, online = _snapshot()
    try:
        checked = settings.validate({**_active_settings(status), **changes})
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    if not mqtt_client.is_connected():
        return jsonify({"error": "not connected to the MQTT broker"}), 503

    # Retained, so the Pi also gets the settings when it starts later.
    mqtt_client.publish(config.TOPIC_SETTINGS, json.dumps(checked), qos=1, retain=True)
    return jsonify({"sent": checked, "device_online": online}), 202


if __name__ == "__main__":
    mqtt_client.connect_async(config.MQTT_BROKER, config.MQTT_PORT, 60)
    mqtt_client.loop_start()
    try:
        # host="0.0.0.0": reachable from other devices in the network
        app.run(host="0.0.0.0", port=config.DASHBOARD_PORT)
    finally:
        mqtt_client.disconnect()
        mqtt_client.loop_stop()
