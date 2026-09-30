import re


ENGINEERING_PATTERNS = {
    "mass": [
        r"\bmass\b",
        r"\bweight\b",
    ],

    "dimensions": [
        r"\bdimension",
        r"\blength\b",
        r"\bwidth\b",
        r"\bheight\b",
        r"\bdiameter\b",
    ],

    "power": [
        r"\bpower\b",
        r"\belectrical power\b",
        r"\bpower consumption\b",
    ],

    "energy": [
        r"\benergy\b",
        r"\bbattery\b",
        r"\bcapacity\b",
    ],

    "thermal": [
        r"\btemperature\b",
        r"\bthermal\b",
        r"\bheating\b",
        r"\bcooling\b",
    ],

    "mobility": [
        r"\bmobility\b",
        r"\bwheel\b",
        r"\bmotor\b",
        r"\bactuator\b",
        r"\btraction\b",
        r"\bspeed\b",
    ],

    "communications": [
        r"\bcommunication\b",
        r"\btelemetry\b",
        r"\bantenna\b",
        r"\bradio\b",
    ],

    "environment": [
        r"\bradiation\b",
        r"\bdust\b",
        r"\bterrain\b",
        r"\bpressure\b",
        r"\batmosphere\b",
    ],

    "physics": [
        r"\bcollision\b",
        r"\bdynamics\b",
        r"\bkinematics\b",
        r"\bautonomous behavior\b",
    ],

    "materials": [
        r"\bmaterial\b",
        r"\baluminum\b",
        r"\baluminium\b",
        r"\btitanium\b",
        r"\bcarbon fiber\b",
        r"\bcomposite\b",
    ],
}


# Only accept actual engineering unit patterns.
MEASUREMENT_PATTERN = re.compile(
    r"""
    (?<![A-Za-z0-9])

    -?\d+(?:\.\d+)?

    \s*

    (?:
        kg
        | g
        | mg
        | m
        | cm
        | mm
        | km
        | W
        | kW
        | MW
        | V
        | kV
        | A
        | mA
        | K
        | °C
        | C
        | km/h
        | m/s
        | Wh
        | kWh
        | Ah
        | kPa
        | MPa
    )

    (?![A-Za-z0-9])
    """,
    re.IGNORECASE
)


def score_evidence(text: str):

    text = text or ""

    category_hits = {}

    for category, patterns in (
        ENGINEERING_PATTERNS.items()
    ):

        hits = 0

        for pattern in patterns:

            matches = re.findall(
                pattern,
                text,
                re.IGNORECASE,
            )

            hits += len(matches)

        category_hits[
            category
        ] = hits

    # Count actual measurements,
    # not arbitrary numbers.
    measurements = (
        MEASUREMENT_PATTERN.findall(
            text
        )
    )

    # Cap the contribution so a huge
    # document doesn't automatically win.
    measurement_score = min(
        len(measurements),
        15,
    )

    category_score = sum(
        min(value, 3)
        for value in category_hits.values()
    )

    final_score = (
        category_score * 3
        + measurement_score
    )

    return {
    "score": final_score,
    "categories": category_hits,
    "measurements": measurements[:25],
    "numerical_evidence": measurements[:25],
    "useful": final_score >= 8
    }