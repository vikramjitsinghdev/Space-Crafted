import json

from nasa_client import NASAClient
from ntrs_client import NTRSClient

from models import Equipment
from equipment_parser import calculate_volume
from storage import save_equipment


def print_equipment(equipment):

    print("\n")
    print("=" * 60)
    print("NASA EQUIPMENT")
    print("=" * 60)

    data = equipment.to_dict()

    for key, value in data.items():

        if value is not None:
            print(
                f"{key:40}: {value}"
            )

    print("=" * 60)


def search_nasa_equipment(name):

    nasa = NASAClient()
    ntrs = NTRSClient()

    print(f"\nSearching NASA for: {name}")

    # --------------------------------------------------
    # 1. Search NASA imagery
    # --------------------------------------------------

    print("\n[1] NASA Image Library")

    try:

        image_results = nasa.search_images(
            name,
            page_size=5
        )

        items = (
            image_results
            .get("collection", {})
            .get("items", [])
        )

        print(
            f"Found {len(items)} NASA image results."
        )

        for item in items:

            data = item.get("data", [])

            if not data:
                continue

            metadata = data[0]

            print(
                "\n -",
                metadata.get("title")
            )

    except Exception as e:

        print(
            "NASA image search failed:",
            e
        )

    # --------------------------------------------------
    # 2. Search NASA Technical Reports
    # --------------------------------------------------

    print("\n[2] NASA Technical Reports Server")

    try:

        results = ntrs.search(
            name
        )

        print(
            "NTRS search completed."
        )

        # The exact response structure can vary,
        # so keep the raw response available.

        with open(
            "ntrs_raw.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results,
                f,
                indent=4
            )

    except Exception as e:

        print(
            "NTRS search failed:",
            e
        )

    # --------------------------------------------------
    # 3. Create initial equipment object
    # --------------------------------------------------

    equipment = Equipment(
        name=name
    )

    # --------------------------------------------------
    # 4. Calculate values that can be calculated
    # --------------------------------------------------

    equipment = calculate_volume(
        equipment
    )

    return equipment


def main():

    print(
        "NASA EQUIPMENT DATA COLLECTOR"
    )

    print(
        "Enter the NASA equipment/tool/instrument "
        "you want to investigate."
    )

    name = input(
        "\nEquipment: "
    ).strip()

    if not name:

        print(
            "No equipment specified."
        )

        return

    equipment = search_nasa_equipment(
        name
    )

    print_equipment(
        equipment
    )

    path = save_equipment(
        equipment
    )

    print(
        f"\nSaved to: {path}"
    )


if __name__ == "__main__":
    main()