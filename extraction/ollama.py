import json
import requests

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_API_KEY
)


SYSTEM_PROMPT = """
You are a NASA engineering-data extraction system.

Extract ONLY information explicitly supported by the supplied NASA text.

NEVER:
- invent values
- estimate missing values
- use outside knowledge
- assume values
- confuse calculated values with NASA-published values

Convert units to SI units where possible.

If a value is not present, return null.

Return ONLY valid JSON.

Schema:

{
    "name": null,
    "description": null,

    "mass_kg": null,

    "length_m": null,
    "width_m": null,
    "height_m": null,
    "diameter_m": null,

    "power_w": null,
    "voltage_v": null,

    "operating_temperature_min_c": null,
    "operating_temperature_max_c": null,

    "manufacturer": null,
    "mission": null,

    "materials": [],

    "specifications": {}
}
"""


def extract_with_ollama(text: str):

    if not OLLAMA_API_KEY:
        raise RuntimeError(
            "OLLAMA_API_KEY is missing from .env"
        )

    url = (
        f"{OLLAMA_BASE_URL.rstrip('/')}"
        "/api/chat"
    )

    headers = {
        "Authorization":
            f"Bearer {OLLAMA_API_KEY}",

        "Content-Type":
            "application/json"
    }

    payload = {

        "model": OLLAMA_MODEL,

        "messages": [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": text
            }
        ],

        "stream": False,

        "format": "json",

        "options": {
            "temperature": 0
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    content = result[
        "message"
    ][
        "content"
    ]

    return json.loads(content)