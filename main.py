from pipelines.equipment_pipeline import (
    EquipmentPipeline,
)


def main():

    equipment_name = input(
        "Enter NASA equipment/vehicle: "
    ).strip()

    if not equipment_name:
        print(
            "Equipment name cannot be empty."
        )
        return

    pipeline = EquipmentPipeline()

    try:
        equipment = pipeline.run(
            equipment_name
        )

        print(
            "\n=============================="
        )

        print(
            "EXTRACTION RESULT"
        )

        print(
            "=============================="
        )

        print(
            f"Name: "
            f"{equipment.name}"
        )

        print(
            f"Mass: "
            f"{equipment.mass_kg} kg"
        )

        print(
            f"Dimensions: "
            f"{equipment.length_m} × "
            f"{equipment.width_m} × "
            f"{equipment.height_m} m"
        )

        print(
            f"Power: "
            f"{equipment.power_w} W"
        )

        print(
            f"Materials: "
            f"{equipment.materials}"
        )

        print(
            f"Calculated: "
            f"{equipment.calculated}"
        )

    except Exception as exc:

        print(
            "\nPipeline failed:"
        )

        print(exc)


if __name__ == "__main__":
    main()