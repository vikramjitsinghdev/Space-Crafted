def cm_to_m(value):
    return None if value is None else value / 100


def mm_to_m(value):
    return None if value is None else value / 1000


def ft_to_m(value):
    return None if value is None else value * 0.3048


def inches_to_m(value):
    return None if value is None else value * 0.0254


def grams_to_kg(value):
    return None if value is None else value / 1000


def pounds_to_kg(value):
    return None if value is None else value * 0.45359237


def normalize_equipment_data(data):
    """
    Normalize known fields to SI units.

    Ollama should preferably already return SI units,
    but this provides a second normalization layer.
    """

    normalized = dict(data)

    return normalized