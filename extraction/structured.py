import re


def extract_value(
    text: str,
    patterns: list[str]
):

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                return float(match.group(1))
            except ValueError:
                pass

    return None


def extract_mass(text):

    return extract_value(
        text,
        [
            r"mass\s*[:=]\s*([\d.]+)\s*kg",
            r"mass\s+of\s+([\d.]+)\s*kg",
            r"([\d.]+)\s*kg\s+mass"
        ]
    )


def extract_power(text):

    return extract_value(
        text,
        [
            r"power\s*[:=]\s*([\d.]+)\s*W",
            r"power\s+of\s+([\d.]+)\s*W",
            r"([\d.]+)\s*W\s+power"
        ]
    )


def extract_length(text):

    return extract_value(
        text,
        [
            r"length\s*[:=]\s*([\d.]+)\s*m",
            r"length\s+of\s+([\d.]+)\s*m"
        ]
    )