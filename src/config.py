# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENCORPORATES_API_KEY = os.getenv("OPENCORPORATES_API_KEY")
OPENCORPORATES_BASE_URL = "https://api.opencorporates.com/v0.4"
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")