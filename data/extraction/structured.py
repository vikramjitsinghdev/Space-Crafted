import re


def _extract_number(patterns, text):
    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        try:
            return float(match.group(1))
        except (ValueError, TypeError):
            continue

    return None


def extract_mass(text):
    return _extract_number(
        [
            r"\bmass\s*(?:of|=|:)?\s*([\d,.]+)\s*kg\b",
            r"\b([\d,.]+)\s*kg\s+(?:mass|weight)\b",
        ],
        text,
    )


def extract_power(text):
    return _extract_number(
        [
            r"\bpower\s*(?:of|=|:)?\s*([\d,.]+)\s*(?:W|watts?)\b",
            r"\b([\d,.]+)\s*(?:W|watts?)\s+(?:power)\b",
        ],
        text,
    )


def extract_voltage(text):
    return _extract_number(
        [
            r"\bvoltage\s*(?:of|=|:)?\s*([\d,.]+)\s*(?:V|volts?)\b",
        ],
        text,
    )


def extract_length(text):
    return _extract_number(
        [
            r"\blength\s*(?:of|=|:)?\s*([\d,.]+)\s*m\b",
        ],
        text,
    )


def extract_width(text):
    return _extract_number(
        [
            r"\bwidth\s*(?:of|=|:)?\s*([\d,.]+)\s*m\b",
        ],
        text,
    )


def extract_height(text):
    return _extract_number(
        [
            r"\bheight\s*(?:of|=|:)?\s*([\d,.]+)\s*m\b",
        ],
        text,
    )


def extract_temperature_range(text):
    pattern = (
        r"(?:temperature|operating temperature)"
        r".{0,50}?"
        r"(-?\d+(?:\.\d+)?)"
        r"\s*(?:°?\s*C)"
        r".{0,50}?"
        r"(-?\d+(?:\.\d+)?)"
        r"\s*(?:°?\s*C)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        return None, None

    return (
        float(match.group(1)),
        float(match.group(2)),
    )


def extract_structured(text):
    temp_min, temp_max = extract_temperature_range(
        text
    )

    return {
        "mass_kg": extract_mass(text),
        "power_w": extract_power(text),
        "voltage_v": extract_voltage(text),
        "length_m": extract_length(text),
        "width_m": extract_width(text),
        "height_m": extract_height(text),
        "operating_temperature_min_c": temp_min,
        "operating_temperature_max_c": temp_max,
    }