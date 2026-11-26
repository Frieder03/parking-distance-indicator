"""Settings that can be changed remotely: warning thresholds and buzzer on/off.

Used by both sides: the dashboard checks a request before it publishes it,
and the Pi checks every message again before it applies it.
"""
import config

FIELDS = ("red_below_cm", "yellow_below_cm", "buzzer")


def current(buzzer_enabled=True):
    """The settings that are active right now."""
    return {
        "red_below_cm": config.RED_BELOW_CM,
        "yellow_below_cm": config.YELLOW_BELOW_CM,
        "buzzer": buzzer_enabled,
    }


def _number(data, key):
    value = data[key]
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be a number")
    return value


def validate(data):
    """Return the checked settings, or raise ValueError with the reason."""
    if not isinstance(data, dict):
        raise ValueError("expected a JSON object")
    unknown = set(data) - set(FIELDS)
    if unknown:
        raise ValueError(f"unknown fields: {', '.join(sorted(unknown))}")
    missing = [key for key in FIELDS if key not in data]
    if missing:
        raise ValueError(f"missing fields: {', '.join(missing)}")

    red = _number(data, "red_below_cm")
    yellow = _number(data, "yellow_below_cm")
    if not config.MIN_DISTANCE_CM <= red < yellow <= config.MAX_DISTANCE_CM:
        raise ValueError(
            f"need {config.MIN_DISTANCE_CM} <= red_below_cm < yellow_below_cm"
            f" <= {config.MAX_DISTANCE_CM}"
        )
    if not isinstance(data["buzzer"], bool):
        raise ValueError("buzzer must be true or false")
    return {"red_below_cm": red, "yellow_below_cm": yellow, "buzzer": data["buzzer"]}


def apply(checked, buzzer):
    """Apply checked settings on the Pi."""
    config.RED_BELOW_CM = checked["red_below_cm"]
    config.YELLOW_BELOW_CM = checked["yellow_below_cm"]
    buzzer.enabled = checked["buzzer"]
