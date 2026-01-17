import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    database_url: str
    interval_seconds: float


def load_settings() -> Settings:
    settings = Settings()

    database_url = os.getenv("LOCAL_DATABASE_URL")
    if not database_url:
        raise RuntimeError("LOCAL_DATABASE_URL is not set in .env")

    interval_seconds = float(os.getenv("INTERVAL_SECONDS", "1"))

    settings.database_url = database_url
    settings.interval_seconds = interval_seconds

    return settings