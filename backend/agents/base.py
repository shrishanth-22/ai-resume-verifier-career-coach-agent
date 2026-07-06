import os
import logging
from openai import OpenAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("multi_agent_recruitment_system")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_openai_client() -> OpenAI:
    if not OPENAI_API_KEY:
        raise RuntimeError("CRITICAL: 'OPENAI_API_KEY' is missing from the environment!")
    return OpenAI(api_key=OPENAI_API_KEY)

def is_mock_mode() -> bool:
    return not OPENAI_API_KEY or OPENAI_API_KEY.startswith("mock_") or OPENAI_API_KEY == "your_openai_api_key_here"
