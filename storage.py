import json
import os

from config import DATA_DIR


def save_equipment(equipment):

    os.makedirs(DATA_DIR, exist_ok=True)

    filename = (
        equipment.name
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        + ".json"
    )

    path = os.path.join(
        DATA_DIR,
        filename
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