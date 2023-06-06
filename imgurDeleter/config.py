import sys
from pathlib import Path

from loguru import logger
from pydantic import BaseSettings, ValidationError


class Settings(BaseSettings):
    client_id: str
    client_secret: str
    username: str
    password: str
    subreddit: str
    removal_urls: list[str]

    class Config:
        root = Path(__file__).parent

        env_file = ".env"


try:
    config = Settings()  # type: ignore
except ValidationError as e:
    logger.error(e.errors)
    logger.error("Validation error loading .env! Check your settings")
    sys.exit(2)


__all__ = ["config"]
