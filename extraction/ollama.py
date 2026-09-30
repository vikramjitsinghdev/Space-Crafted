import json
import requests

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
    OLLAMA_API_KEY,
)


SYSTEM_PROMPT = """
You are a NASA engineering-data extraction system.

Your job is to extract engineering information from supplied
NASA document evidence.

============================================================
CANONICAL EQUIPMENT IDENTITY
============================================================

The requested equipment name is supplied separately by the
application.

The requested equipment is the CANONICAL TARGET.

NEVER replace the requested equipment with another:

- vehicle
- rover
- spacecraft
- helicopter
- instrument
- subsystem
- component
- demonstration unit
- test article
- software system
- facility
- unrelated hardware

A NASA document may mention many different pieces of equipment.

Extract information ONLY when the supplied evidence clearly
applies to the requested equipment.

If the evidence discusses multiple pieces of equipment and it
is unclear which one a specification belongs to, DO NOT assign
that specification to the requested equipment.

Return null instead.

The "name" field must be the requested equipment name when
the evidence supports that the requested equipment is being
discussed.

Do NOT choose the name of another object mentioned in the
document.

============================================================
STRICT EVIDENCE RULES
============================================================

1. Use ONLY information explicitly supported by the supplied
   evidence.

2. NEVER use outside knowledge.

3. NEVER guess missing values.

4. NEVER estimate values.

5. NEVER infer a specification from context unless the evidence
   explicitly supports it.

6. If a value is not explicitly supported, return null.

7. Preserve the distinction between published/document evidence
   and calculated information.

8. Convert units to SI units only when the conversion is
   unambiguous.

9. Every extracted specification must have supporting evidence
   whenever the document provides it.

10. Do not invent equipment specifications.

11. Do not transfer specifications from another vehicle,
    subsystem, component, instrument, or test article.

12. If the document does not contain useful information about
    the requested equipment, return null for unsupported fields.

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Use exactly this structure:

{
    "name": null,
    "description": null,
    "mission": null,
    "manufacturer": null,
    "category": null,

    "mass_kg": null,
    "length_m": null,
    "width_m": null,
    "height_m": null,
    "diameter_m": null,

    "power_w": null,
    "voltage_v": null,

    "operating_temperature_min_c": null,
    "operating_temperature_max_c": null,

    "materials": [],

    "specifications": {},

    "evidence": {}
}

============================================================
EVIDENCE FORMAT
============================================================

The evidence object should contain only fields for which the
document explicitly provides supporting evidence.

Example:

{
    "mass_kg": 1025,
    "evidence": {
        "mass_kg": "The rover mass is 1025 kg."
    }
}

If the document does not provide mass:

{
    "mass_kg": null
}

Do not create evidence for unsupported values.

============================================================
IMPORTANT
============================================================

The application will provide:

REQUESTED EQUIPMENT:
<equipment name>

DOCUMENT EVIDENCE:
<NASA evidence>

Treat the requested equipment as authoritative.

Your job is to extract specifications ABOUT that equipment,
not to identify a different object from the document.
"""


def extract_with_ollama(
    text: str,
    equipment_name: str,
):
    """
    Extract NASA engineering information using Ollama.

    The equipment_name is explicitly supplied to the model so
    that the requested equipment remains the canonical identity.
    """

    if not OLLAMA_API_KEY:
        raise RuntimeError(
            "OLLAMA_API_KEY is missing from .env"
        )

    url = (
        f"{OLLAMA_BASE_URL.rstrip('/')}"
        "/api/chat"
    )

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    user_prompt = f"""
REQUESTED EQUIPMENT:
{equipment_name}

============================================================
NASA DOCUMENT EVIDENCE
============================================================

{text}

============================================================
EXTRACTION TASK
============================================================

Extract ONLY engineering information that explicitly applies
to:

{equipment_name}

If another vehicle, subsystem, instrument, component,
demonstration unit, or test article appears in the evidence,
DO NOT extract its specifications as specifications of
{equipment_name}.

The canonical equipment name for this extraction is:

{equipment_name}
"""

    payload = {
        "model": OLLAMA_MODEL,

        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],

        "stream": False,

        "format": "json",

        "options": {
            "temperature": 0,
        },
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    result = response.json()

    content = result["message"]["content"]

    try:
        return json.loads(content)

    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Ollama returned invalid JSON."
        ) from exc