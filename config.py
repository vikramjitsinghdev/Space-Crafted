import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "https://ollama.com"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "gpt-oss:120b-cloud"
)

OLLAMA_API_KEY = os.getenv(
    "OLLAMA_API_KEY"
)

RAW_DATA_DIR = "data/raw"
EQUIPMENT_DATA_DIR = "data/equipment"

NASA_IMAGES_API = "https://images-api.nasa.gov"
NTRS_API = "https://ntrs.nasa.gov/api"