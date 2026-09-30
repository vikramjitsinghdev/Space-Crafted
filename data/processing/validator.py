def validate_equipment_data(data):
    warnings = []

    positive_fields = [
        "mass_kg",
        "length_m",
        "width_m",
        "height_m",
        "diameter_m",
        "power_w",
        "voltage_v",
    ]

    for field in positive_fields:

        value = data.get(field)

        if value is None:
            continue

        if value < 0:
            warnings.append(
                f"{field} cannot be negative."
            )

    temperature_min = data.get(
        "operating_temperature_min_c"
    )

    temperature_max = data.get(
        "operating_temperature_max_c"
    )

    if (
        temperature_min is not None
        and temperature_max is not None
        and temperature_min > temperature_max
    ):
        warnings.append(
            "Minimum operating temperature "
            "is greater than maximum."
        )

    return warnings