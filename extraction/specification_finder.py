import re

SPECIFICATION_TERMS = [
    "mass",
    "weight",
    "dimension",
    "dimensions",
    "length",
    "width",
    "height",
    "diameter",
    "volume",
    "power",
    "electrical power",
    "voltage",
    "current",
    "temperature",
    "thermal",
    "energy",
    "battery",
    "capacity",
    "material",
    "size"
]


def find_relevant_pages(
    pages,
    context_chars=1500
):

    relevant = []

    for page in pages:

        text = page["text"]

        lower = text.lower()

        matches = []

        for term in SPECIFICATION_TERMS:

            if term in lower:

                matches.append(term)

        if not matches:
            continue

        # Keep the page plus some context.
        snippet = text[:context_chars]

        relevant.append({

            "page": page["page"],

            "matched_terms": matches,

            "text": snippet
        })

    return relevant