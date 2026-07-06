import os
import sys
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("CRITICAL: 'OPENAI_API_KEY' is missing from the environment or .env file! Application startup halted.")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import app
