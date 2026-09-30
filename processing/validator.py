def validate_equipment(
    equipment
):

    warnings = []

    if (
        equipment.mass_kg is not None
        and equipment.mass_kg < 0
    ):

        warnings.append(
            "Mass cannot be negative."
        )

    if (
        equipment.power_w is not None
        and equipment.power_w < 0
    ):

        warnings.append(
            "Power cannot be negative."
        )

    if (
        equipment.length_m is not None
        and equipment.length_m <= 0
    ):

        warnings.append(
            "Length must be positive."
        )

    if (
        equipment.width_m is not None
        and equipment.width_m <= 0
    ):

        warnings.append(
            "Width must be positive."
        )

    if (
        equipment.height_m is not None
        and equipment.height_m <= 0
    ):

        warnings.append(
            "Height must be positive."
        )

    return warnings