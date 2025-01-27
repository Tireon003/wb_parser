from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    RMQ_USER: str
    RMQ_PASS: str
    RMQ_HOST: str
    RMQ_PROTOCOL: str
    LOGGER_QUEUE_NAME: str

    LOG_LEVEL: str
    LOG_FORMAT: str

    @property
    def rmq_url(self) -> str:
        return f"{self.RMQ_PROTOCOL}://{self.RMQ_USER}:{self.RMQ_PASS}@{self.RMQ_HOST}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
