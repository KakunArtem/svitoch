import logging
from datetime import tzinfo
from logging.config import dictConfig
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, BaseSettings
from pytz import timezone


class Config(BaseSettings):
    """
    Variables contained in this model will attempt to load from .env or environment and if variable is missing,
    it will throw exception.
    """

    APP_VERSION: str = "0.0.1"
    LOG_LEVEL: str = "INFO"
    TIMEZONE: tzinfo = timezone("Europe/Kyiv")

    OPENAI_GENERATION_MODEL_NAME: str
    OPENAI_API_KEY: str

    PROJECT_ROOT: Path = Path(__file__).absolute().parent.parent

    class Config:
        env_file = find_dotenv(".env", raise_error_if_not_found=True)


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "svitoch-rest-api"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["default"], "level": LOG_LEVEL},
    }


load_dotenv(find_dotenv(".env", raise_error_if_not_found=True))
config = Config()  # type: ignore

# Setup logger
dictConfig(LogConfig(LOG_LEVEL=config.LOG_LEVEL).dict())
logger = logging.getLogger("svitoch-rest-api")
