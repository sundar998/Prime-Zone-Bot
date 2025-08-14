import os
from typing import List

API_ID = int(os.getenv("API_ID", "17428722"))
API_HASH = os.getenv("API_HASH", "3a1f13be61cae6f67ecf03fef325349e")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID", "-1002549707609"))
ADMIN_ID = int(os.getenv("ADMIN_ID", "7547946252"))
PICS = (os.environ.get("PICS", "https://envs.sh/2iq.jpg")).split()
LOG_CHNL = int(os.getenv("LOG_CHNL", "-1002458686235"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "mrrandom4k") # Without @
IS_FSUB = bool(os.environ.get("FSUB", True ))
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1002275599146").split()))
DATABASE_CHANNEL_LOG = int(os.getenv("DATABASE_CHANNEL_LOG", "-1002458686235"))
FREE_VIDEO_DURATION = int(os.getenv("FREE_VIDEO_DURATION", "240"))
