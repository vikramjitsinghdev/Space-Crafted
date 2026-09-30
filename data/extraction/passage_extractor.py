import re


ENGINEERING_PATTERNS = {
    "physical": [
        r"\bmass\b",
        r"\bweight\b",
        r"\bdimension",
        r"\blength\b",
        r"\bwidth\b",
        r"\bheight\b",
        r"\bdiameter\b",
        r"\bsize\b",
        r"\bkg\b",
        r"\bkilogram",
        r"\bmm\b",
        r"\bcm\b",
        r"\bm\b",
    ],

    "power": [
        r"\bpower\b",
        r"\bwatt",
        r"\bkilowatt",
        r"\bvoltage\b",
        r"\bvolt\b",
        r"\bcurrent\b",
        r"\bamp",
        r"\bbattery\b",
        r"\belectrical\b",
    ],

    "thermal": [
        r"\btemperature\b",
        r"\bthermal\b",
        r"\bheat\b",
        r"\bcooling\b",
        r"\bheater\b",
        r"\boperating temperature\b",
    ],

    "mobility": [
        r"\bwheel\b",
        r"\bwheels\b",
        r"\bmotor\b",
        r"\bactuator\b",
        r"\bmobility\b",
        r"\btraction\b",
        r"\bspeed\b",
        r"\bdrive\b",
    ],

    "communication": [
        r"\bantenna\b",
        r"\bcommunication\b",
        r"\bcommunications\b",
        r"\btelemetry\b",
        r"\bradio\b",
        r"\bbandwidth\b",
        r"\bdata rate\b",
    ],

    "operations": [
        r"\boperat",
        r"\bduty cycle\b",
        r"\blifetime\b",
        r"\brange\b",
        r"\bcapacity\b",
        r"\bmission duration\b",
        r"\boperational\b",
    ],

    "materials": [
        r"\bmaterial\b",
        r"\baluminum\b",
        r"\baluminium\b",
        r"\btitanium\b",
        r"\bsteel\b",
        r"\bcomposite\b",
        r"\bcarbon fiber\b",
    ],
}


def classify_text(text: str) -> set[str]:
    lower = text.lower()

    categories = set()

    for category, patterns in ENGINEERING_PATTERNS.items():

        for pattern in patterns:

            if re.search(pattern, lower):
                categories.add(category)
                break

    return categories


def score_passage(text: str) -> int:
    categories = classify_text(text)

    score = len(categories) * 5

    # Strong evidence indicators
    if re.search(
        r"\d+(\.\d+)?\s*(kg|g|lb|m|cm|mm|w|kw|v|°c|c)",
        text,
        re.IGNORECASE,
    ):
        score += 15

    # Specification-like syntax
    if re.search(
        r"(mass|power|voltage|temperature|length|width|height)"
        r"\s*(is|was|of|=|:)",
        text,
        re.IGNORECASE,
    ):
        score += 15

    return score


def extract_passages(
    pages,
    context_chars: int = 700,
    minimum_score: int = 8,
):
    passages = []

    for page in pages:

        text = page["text"]

        if not text:
            continue

        lower = text.lower()

        matches = []

        for category, patterns in ENGINEERING_PATTERNS.items():

            for pattern in patterns:

                for match in re.finditer(
                    pattern,
                    lower,
                    re.IGNORECASE,
                ):
                    matches.append(
                        (
                            match.start(),
                            match.end(),
                            category,
                        )
                    )

        if not matches:
            continue

        # Merge nearby matches into evidence windows
        windows = []

        for start, end, category in matches:

            window_start = max(
                0,
                start - context_chars
            )

            window_end = min(
                len(text),
                end + context_chars
            )

            windows.append(
                {
                    "start": window_start,
                    "end": window_end,
                    "category": category,
                }
            )

        windows.sort(key=lambda x: x["start"])

        merged = []

        for window in windows:

            if not merged:
                merged.append(window)
                continue

            previous = merged[-1]

            if window["start"] <= previous["end"]:
                previous["end"] = max(
                    previous["end"],
                    window["end"],
                )

            else:
                merged.append(window)

        for window in merged:

            passage_text = text[
                window["start"]:window["end"]
            ].strip()

            score = score_passage(passage_text)

            if score < minimum_score:
                continue

            categories = classify_text(
                passage_text
            )

            passages.append({
                "page": page["page"],
                "text": passage_text,
                "categories": sorted(categories),
                "score": score,
            })

    passages.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return passages