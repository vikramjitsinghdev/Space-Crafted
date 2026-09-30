def calculate_volume(
    length,
    width,
    height
):

    if None in (
        length,
        width,
        height
    ):
        return None

    return (
        length *
        width *
        height
    )


def calculate_footprint(
    length,
    width
):

    if None in (
        length,
        width
    ):
        return None

    return length * width


def calculate_daily_energy(
    power_w
):

    if power_w is None:
        return None

    return (
        power_w *
        24
    ) / 1000