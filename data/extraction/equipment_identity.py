import re


EQUIPMENT_ALIASES = {
    "perseverance rover": [
        "perseverance rover",
        "perseverance",
        "mars 2020 rover",
        "mars 2020 perseverance rover",
        "m2020 rover",
    ],

    "curiosity rover": [
        "curiosity rover",
        "curiosity",
        "mars science laboratory",
        "msl rover",
    ],

    "opportunity rover": [
        "opportunity rover",
        "opportunity",
        "mars exploration rover",
        "mer-b",
    ],

    "spirit rover": [
        "spirit rover",
        "spirit",
        "mars exploration rover",
        "mer-a",
    ],

    "ingenuity helicopter": [
        "ingenuity",
        "ingenuity helicopter",
        "mars helicopter",
    ],
}


def normalize_name(name: str):
    return " ".join(
        name.lower().split()
    )


def get_aliases(equipment_name: str):
    normalized = normalize_name(
        equipment_name
    )

    # Known equipment
    if normalized in EQUIPMENT_ALIASES:
        return EQUIPMENT_ALIASES[
            normalized
        ]

    # Generic fallback
    return []


def find_identity_matches(
    equipment_name: str,
    text: str,
):
    """
    Find explicit mentions of the requested
    equipment in document text.
    """

    text_lower = text.lower()

    aliases = get_aliases(
        equipment_name
    )

    matches = []

    for alias in aliases:

        if alias in text_lower:
            matches.append(alias)

    return matches


def title_matches_equipment(
    equipment_name: str,
    title: str,
):
    """
    Determine whether the document title
    explicitly identifies the requested equipment.
    """

    matches = find_identity_matches(
        equipment_name,
        title,
    )

    return len(matches) > 0


def document_matches_equipment(
    equipment_name: str,
    title: str,
    text: str,
):
    """
    Strong identity check.

    The requested equipment must be explicitly
    represented in either the title or document text.
    """

    title_matches = find_identity_matches(
        equipment_name,
        title,
    )

    text_matches = find_identity_matches(
        equipment_name,
        text,
    )

    return {
        "matches": list(
            set(
                title_matches
                + text_matches
            )
        ),
        "title_match": bool(
            title_matches
        ),
        "text_match": bool(
            text_matches
        ),
        "matched": bool(
            title_matches
            or text_matches
        ),
    }