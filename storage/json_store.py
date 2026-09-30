import json
import os


def save_equipment(
    equipment,
    directory="data/equipment"
):

    os.makedirs(
        directory,
        exist_ok=True
    )

    filename = (
        equipment.name
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    path = os.path.join(
        directory,
        filename + ".json"
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            equipment.to_dict(),
            f,
            indent=4
        )

    return path