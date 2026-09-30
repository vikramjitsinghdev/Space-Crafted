def calculate_bounding_volume(
    length,
    width,
    height,
):
    if None in (
        length,
        width,
        height,
    ):
        return None

    return length * width * height


def calculate_footprint(
    length,
    width,
):
    if None in (
        length,
        width,
    ):
        return None

    return length * width


def calculate_daily_energy(power_w):
    if power_w is None:
        return None

    return (
        power_w * 24
    ) / 1000


def calculate_all(data):
    calculated = {}

    volume = calculate_bounding_volume(
        data.get("length_m"),
        data.get("width_m"),
        data.get("height_m"),
    )

    if volume is not None:
        calculated[
            "bounding_volume_m3"
        ] = volume

    footprint = calculate_footprint(
        data.get("length_m"),
        data.get("width_m"),
    )

    if footprint is not None:
        calculated[
            "footprint_m2"
        ] = footprint

    daily_energy = calculate_daily_energy(
        data.get("power_w")
    )

    if daily_energy is not None:
        calculated[
            "daily_energy_kwh"
        ] = daily_energy

    return calculated