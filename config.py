import os
from dotenv import load_dotenv

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

NASA_BASE_URL = "https://api.nasa.gov"
NTRS_BASE_URL = "https://ntrs.nasa.gov/api"

DATA_DIR = "data/equipment"