import re


POSITIVE_TERMS = {
    # Engineering
    "engineering": 15,
    "engineered": 10,
    "design": 12,
    "development": 8,
    "architecture": 10,
    "system": 8,
    "subsystem": 10,

    # Specifications
    "specification": 20,
    "specifications": 20,
    "requirements": 15,
    "dimensions": 15,
    "mass": 15,
    "weight": 10,

    # Power
    "power": 12,
    "electrical": 10,
    "battery": 12,
    "voltage": 10,

    # Mechanical
    "mechanical": 10,
    "mobility": 15,
    "actuator": 10,
    "wheel": 8,
    "motor": 8,

    # Thermal
    "thermal": 10,
    "temperature": 8,

    # Operations
    "operations": 8,
    "operational": 10,
    "performance": 8,

    # Spacecraft
    "rover": 10,
    "spacecraft": 15,
    "lander": 12,
    "payload": 10,
    "instrument": 8,

    # Mission hardware
    "hardware": 12,
    "equipment": 15,
    "component": 10,
}


NEGATIVE_TERMS = {
    "geology": -12,
    "geologic": -12,
    "geological": -12,
    "biosignature": -15,
    "sediment": -12,
    "sedimentary": -12,
    "mineralogy": -12,
    "mineral": -8,
    "rock": -8,
    "rocks": -8,
    "stratigraphy": -12,
    "petrology": -12,
    "atmospheric": -5,
    "climate": -5,
}


HIGH_VALUE_PHRASES = {
    "technical report": 15,
    "engineering design": 20,
    "system design": 18,
    "design and development": 15,
    "flight system": 15,
    "flight hardware": 20,
    "rover design": 20,
    "rover engineering": 20,
    "spacecraft design": 20,
    "instrument design": 15,
    "power system": 15,
    "thermal control": 15,
    "mobility system": 15,
    "electrical system": 15,
}


def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.lower()).strip()


def score_document(title: str, description: str = "") -> int:
    text = normalize_title(f"{title} {description}")

    score = 0

    for term, points in POSITIVE_TERMS.items():
        if re.search(rf"\b{re.escape(term)}\b", text):
            score += points

    for term, points in NEGATIVE_TERMS.items():
        if re.search(rf"\b{re.escape(term)}\b", text):
            score += points

    for phrase, points in HIGH_VALUE_PHRASES.items():
        if phrase in text:
            score += points

    return score


def rank_documents(results, title_function, id_function):
    ranked = []

    for result in results:
        title = title_function(result)
        citation_id = id_function(result)

        if not title:
            continue

        description = ""

        if isinstance(result, dict):
            description = (
                result.get("description")
                or result.get("abstract")
                or result.get("abstractText")
                or ""
            )

        score = score_document(title, description)

        ranked.append({
            "score": score,
            "title": title,
            "citation_id": citation_id,
            "result": result,
        })

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return ranked

def deduplicate_documents(ranked_documents):
    """
    Remove duplicate documents based on normalized titles.
    """

    seen_titles = set()

    unique = []

    for document in ranked_documents:

        title = (
            document.get("title")
            or ""
        )

        normalized = (
            " ".join(
                title.lower().split()
            )
        )

        if normalized in seen_titles:
            continue

        seen_titles.add(
            normalized
        )

        unique.append(
            document
        )

    return unique