import re


DOCUMENT_CATEGORIES = {
    "hardware": [
        "hardware",
        "equipment",
        "component",
        "instrument",
        "rover",
        "spacecraft",
        "lander",
        "vehicle",
    ],

    "engineering": [
        "engineering",
        "design",
        "architecture",
        "subsystem",
        "mechanical",
        "electrical",
        "structural",
        "configuration",
    ],

    "performance": [
        "performance",
        "capability",
        "range",
        "speed",
        "capacity",
        "efficiency",
    ],

    "mobility": [
        "mobility",
        "wheel",
        "wheels",
        "traction",
        "drive",
        "motor",
        "actuator",
        "navigation",
        "terrain",
    ],

    "thermal": [
        "thermal",
        "temperature",
        "heating",
        "cooling",
        "heater",
    ],

    "power": [
        "power",
        "battery",
        "electrical",
        "voltage",
        "energy",
    ],

    "communications": [
        "communication",
        "communications",
        "radio",
        "antenna",
        "telemetry",
        "data rate",
    ],

    "operations": [
        "operations",
        "operational",
        "mission planning",
        "command",
        "procedure",
        "activity planning",
    ],

    "physics": [
        "collision",
        "dynamics",
        "kinematics",
        "simulation",
        "physics",
        "autonomous behavior",
    ],

    "environment": [
        "environment",
        "radiation",
        "dust",
        "terrain",
        "temperature",
        "pressure",
        "mars surface",
        "lunar surface",
    ],

    "science": [
        "geology",
        "geologic",
        "geological",
        "mineralogy",
        "biosignature",
        "sediment",
        "sedimentary",
        "petrology",
    ],
}


# Things that are often related to a mission
# but aren't themselves equipment specifications.
SOFTWARE_TERMS = {
    "software",
    "software system",
    "application",
    "planning software",
    "activity planning software",
    "interface",
    "user interface",
    "database",
    "information system",
}


def classify_document(
    title: str,
    text: str = "",
):
    """
    Classify a NASA document based on its title and text.
    """

    combined = (
        f"{title}\n{text}"
    ).lower()

    scores = {}

    for category, terms in DOCUMENT_CATEGORIES.items():

        score = 0

        for term in terms:

            if term in combined:
                score += 1

        scores[category] = score

    software_score = 0

    for term in SOFTWARE_TERMS:

        if term in combined:
            software_score += 1

    scores["software"] = software_score

    return scores


def get_document_type(scores):
    """
    Return the dominant document category.
    """

    filtered = {
        key: value
        for key, value in scores.items()
        if key != "science"
    }

    if not filtered:
        return "unknown"

    return max(
        filtered,
        key=filtered.get,
    )


def is_simulation_useful(
    title: str,
    text: str,
    requested_equipment: str,
):
    """
    Determine whether a document appears useful
    for SpaceCrafted simulation extraction.
    """

    scores = classify_document(
        title,
        text,
    )

    combined = (
        f"{title}\n{text}"
    ).lower()

    equipment_words = (
        requested_equipment
        .lower()
        .split()
    )

    equipment_matches = sum(
        1
        for word in equipment_words
        if len(word) > 2
        and word in combined
    )

    useful_categories = [
        "hardware",
        "engineering",
        "performance",
        "mobility",
        "thermal",
        "power",
        "communications",
        "physics",
        "environment",
    ]

    useful_score = sum(
        scores.get(category, 0)
        for category in useful_categories
    )

    # Software-heavy documents are not automatically
    # useless, but should require stronger evidence.
    software_penalty = (
        scores.get("software", 0) * 2
    )

    final_score = (
        equipment_matches * 5
        + useful_score
        - software_penalty
    )

    return {
        "useful": final_score >= 5,
        "score": final_score,
        "document_type": get_document_type(
            scores
        ),
        "categories": scores,
    }