from models.equipment import (
    Equipment,
    Source
)

from collectors.nasa_api import (
    NASAClient
)

from collectors.ntrs import (
    NTRSClient
)

from extraction.structured import (
    extract_mass,
    extract_power,
    extract_length
)

from extraction.ollama import (
    extract_with_ollama
)

from processing.calculations import (
    calculate_volume,
    calculate_footprint,
    calculate_daily_energy
)

from processing.validator import (
    validate_equipment
)

from storage.json_store import (
    save_equipment
)


def merge_ai_data(
    equipment,
    data
):

    for field in [
        "description",
        "mass_kg",
        "length_m",
        "width_m",
        "height_m",
        "diameter_m",
        "power_w",
        "voltage_v",
        "operating_temperature_min_c",
        "operating_temperature_max_c",
        "manufacturer",
        "mission"
    ]:

        value = data.get(field)

        if (
            getattr(equipment, field)
            is None
            and value is not None
        ):

            setattr(
                equipment,
                field,
                value
            )

    materials = data.get(
        "materials"
    )

    if materials:
        equipment.materials = materials

    specs = data.get(
        "specifications"
    )

    if specs:
        equipment.specifications.update(
            specs
        )

    equipment.ai_extracted = True

    if "ollama" not in equipment.extraction_methods:

        equipment.extraction_methods.append(
            "ollama"
        )


from collectors.ntrs import NTRSClient
from collectors.ntrs_parser import (
    extract_results,
    extract_citation_id,
    extract_title
)


def test_ntrs_retrieval(
    equipment_name
):

    ntrs = NTRSClient()

    print(
        "\nSearching NTRS..."
    )

    search_results = ntrs.search(
        equipment_name,
        size=10
    )

    results = extract_results(
        search_results
    )

    print(
        f"\nFound {len(results)} results."
    )

    for index, result in enumerate(
        results
    ):

        citation_id = extract_citation_id(
            result
        )

        title = extract_title(
            result
        )

        print(
            f"\n[{index + 1}]"
        )

        print(
            "Title:",
            title
        )

        print(
            "Citation ID:",
            citation_id
        )

    return results


def main():

    print(
        "SPACECRAFTED NASA RETRIEVAL TEST"
    )

    name = input(
        "\nEquipment: "
    ).strip()

    test_ntrs_retrieval(
        name
    )


if __name__ == "__main__":
    main()