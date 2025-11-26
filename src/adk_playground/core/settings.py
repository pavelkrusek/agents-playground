import os

from dotenv import load_dotenv, find_dotenv
from google.adk.models import Gemini
from google.genai import types

load_dotenv(find_dotenv(), override=False)

MODEL_NAME = os.getenv("MODEL", "gemini-2.5-flash-lite")
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
APP_NAME = "agents"

if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY/GOOGLE_API_KEY in environment/.env")

RETRY = types.HttpRetryOptions(
    attempts=3,
    exp_base=2,
    initial_delay=0.5,
    http_status_codes=[429, 500, 503, 504],
)

MODEL = Gemini(model=MODEL_NAME, retry_options=RETRY)
