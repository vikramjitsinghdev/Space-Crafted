import json
import os
import re


def safe_filename(name: str):
    name = name.lower()

    name = re.sub(
        r"[^a-z0-9_-]+",
        "_",
        name,
    )

    return name.strip("_")


def save_equipment(
    equipment,
    directory="data/equipment",
):
    os.makedirs(
        directory,
        exist_ok=True,
    )

    filename = (
        safe_filename(equipment.name)
        + ".json"
    )

    path = os.path.join(
        directory,
        filename,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            equipment.to_dict(),
            file,
            indent=4,
            ensure_ascii=False,
        )

    return path