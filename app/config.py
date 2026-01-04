import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Aura LLM API"
    API_VERSION = "v1"

    # LLM
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")

    # Discord
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

settings = Settings()
