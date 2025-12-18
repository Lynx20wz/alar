import sys

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB_PATH: str

    JWT_SECRET: str
    JWT_MIN: int
    JWT_HOUR: int
    JWT_DAY: int
    JWT_ALGORITHM: str

    @property
    def JWT_ACCESS_TOKEN_EXPIRATION_TIME(self) -> int:
        return self.JWT_MIN + self.JWT_HOUR * 60 + self.JWT_DAY * 24 * 60

    model_config = SettingsConfigDict(
        env_file='.env',
    )


config = Config()  # type: ignore

logger.remove()
logger.add(
    sink=sys.stdout,
    level='DEBUG',
    format='{time:H:mm:ss} | "{function}" | {line} ({module}) | <level>{level}</level> | {message}',
)
