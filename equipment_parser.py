import re

from models import Equipment


def extract_number(value):

    if value is None:
        return None

    match = re.search(
        r"[-+]?\d*\.?\d+",
        str(value)
    )

    if not match:
        return None

    return float(match.group())


def calculate_volume(equipment):

    if (
        equipment.length_m is not None
        and equipment.width_m is not None
        and equipment.height_m is not None
    ):

        equipment.volume_m3 = (
            equipment.length_m
            * equipment.width_m
            * equipment.height_m
        )

    return equipment


def normalize_length(value, unit):

    value = extract_number(value)

    if value is None:
        return None

    unit = unit.lower()

    if unit in ["m", "meter", "meters"]:
        return value

    if unit in ["cm", "centimeter", "centimeters"]:
        return value / 100

    if unit in ["mm", "millimeter", "millimeters"]:
        return value / 1000

    if unit in ["ft", "feet", "foot"]:
        return value * 0.3048

    if unit in ["in", "inch", "inches"]:
        return value * 0.0254

    return value


def normalize_mass(value, unit):

    value = extract_number(value)

    if value is None:
        return None

    unit = unit.lower()

    if unit in ["kg", "kilogram", "kilograms"]:
        return value

    if unit in ["g", "gram", "grams"]:
        return value / 1000

    if unit in ["lb", "lbs", "pound", "pounds"]:
        return value * 0.45359237

    return value