from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):

    PARSER_SERVICE_HOST: str
    PARSER_SERVICE_PORT: int

    LOG_LEVEL: Literal[
        "NOTSET",
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]
    LOG_FORMAT: str

    PATH_TO_CREDENTIALS: str
    GOOGLE_SHEET_NAME: str

    PARSER_SERVICE_HOST: str
    PARSER_SERVICE_PORT: int

    WB_URL: str

    SELENIUM_HOST: str
    SELENIUM_PORT: int
    USER_AGENT: str

    @property
    def selenium_url(self) -> str:
        return f"http://{self.SELENIUM_HOST}:{self.SELENIUM_PORT}/wd/hub"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
