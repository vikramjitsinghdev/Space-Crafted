import json
from openai import OpenAI

from config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY
)


EXTRACTION_PROMPT = """
You are extracting engineering specifications from NASA documentation.

Extract ONLY information explicitly supported by the provided text.

Do not guess.

Return valid JSON using this structure:

{
    "name": null,
    "length_m": null,
    "width_m": null,
    "height_m": null,
    "diameter_m": null,
    "mass_kg": null,
    "power_w": null,
    "voltage_v": null,
    "material": null,
    "manufacturer": null,
    "operating_temperature_min_c": null,
    "operating_temperature_max_c": null,
    "additional_specs": {}
}

Convert units to SI where possible.

If a value is not present, use null.

Text:
"""


def extract_equipment_specs(text):

    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY not configured."
        )

    response = client.responses.create(

        model="gpt-5.6",

        input=EXTRACTION_PROMPT + text
    )

    raw = response.output_text

    return json.loads(raw)