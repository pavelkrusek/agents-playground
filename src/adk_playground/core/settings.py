import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=False)

MODEL = os.getenv("MODEL", "gemini-2.5-flash-lite")
API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
APP_NAME = "agents"

if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY/GOOGLE_API_KEY in environment/.env")
