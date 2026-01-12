import os
from typing import List

API_ID = int(os.getenv("API_ID", "32981901"))
API_HASH = os.getenv("API_HASH", "f110603912d863a8049888ab3bf5e5d0")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_URI = os.getenv("MONGO_URI", "")

# 🔹 Existing database channel (USED BY /getvideos)
DATABASE_CHANNEL_ID = int(os.getenv("DATABASE_CHANNEL_ID", "-1003522088853"))

# 🔹 NEW: File Store database channel (USED BY /store)
FILESTORE_DB_CHANNEL = int(os.getenv("FILESTORE_DB_CHANNEL", "-1003567393317"))

ADMIN_ID = int(os.getenv("ADMIN_ID", "8054916377"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "srmoviesowner")  # Without @

PICS = (os.environ.get("PICS", "https://envs.sh/2iq.jpg")).split()

LOG_CHNL = int(os.getenv("LOG_CHNL", "-1003494265148"))
DATABASE_CHANNEL_LOG = int(os.getenv("DATABASE_CHANNEL_LOG", "-1002862453522"))

IS_FSUB = bool(os.environ.get("FSUB", True))
AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNEL", "-1003402999196").split()))

FREE_VIDEO_DURATION = int(os.getenv("FREE_VIDEO_DURATION", "240"))
