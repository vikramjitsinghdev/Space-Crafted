import re


SPECIFICATION_PATTERNS = {

    "mass": [
        r"\bmass\b",
        r"\bweight\b",
        r"\bkg\b",
        r"\bkilograms?\b"
    ],

    "dimensions": [
        r"\bdimension",
        r"\blength\b",
        r"\bwidth\b",
        r"\bheight\b",
        r"\bdiameter\b",
        r"\bsize\b",
        r"\bmm\b",
        r"\bcm\b",
        r"\bmeters?\b"
    ],

    "power": [
        r"\bpower\b",
        r"\bwatt",
        r"\bwatts?\b",
        r"\bkilowatt",
        r"\bvoltage\b",
        r"\bcurrent\b",
        r"\bbattery\b"
    ],

    "thermal": [
        r"\btemperature\b",
        r"\bthermal\b",
        r"\bheat\b",
        r"\bcooling\b"
    ],

    "mechanical": [
        r"\bmechanical\b",
        r"\bstructure\b",
        r"\bmechanism\b",
        r"\bactuator\b",
        r"\bwheel\b",
        r"\barm\b",
        r"\bmount\b"
    ],

    "materials": [
        r"\bmaterial\b",
        r"\baluminum\b",
        r"\baluminium\b",
        r"\btitanium\b",
        r"\bsteel\b",
        r"\bcomposite\b"
    ],

    "performance": [
        r"\bperformance\b",
        r"\bcapacity\b",
        r"\bspeed\b",
        r"\brange\b",
        r"\boperating\b",
        r"\blifetime\b"
    ]
}


def classify_page(text: str):

    lower = text.lower()

    categories = []

    for category, patterns in (
        SPECIFICATION_PATTERNS.items()
    ):

        for pattern in patterns:

            if re.search(
                pattern,
                lower
            ):

                categories.append(
                    category
                )

                break

    return categories


def find_relevant_pages(
    pages
):

    relevant = []

    for page in pages:

        categories = classify_page(
            page["text"]
        )

        if not categories:
            continue

        relevant.append({

            "page": page["page"],

            "categories": categories,

            "text": page["text"]

        })

    return relevant