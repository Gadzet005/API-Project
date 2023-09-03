import os

from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN", "invalid api token")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

BACKEND_HOST = os.getenv("BACKEND_HOST", "backend")
BACKEND_PORT = os.getenv("BACKEND_PORT", 8000)
BACKEND_DOMEN = BACKEND_HOST + ":" + BACKEND_PORT
