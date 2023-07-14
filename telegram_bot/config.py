import os

from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.getenv("TELEGRAM_BOT_API_TOKEN", "invalid api token")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
BACKEND_DOMEN = os.getenv("BACKEND_DOMEN", "127.0.0.1:8000")
