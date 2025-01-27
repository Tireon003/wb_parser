from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_GATEWAY_HOST: str
    API_GATEWAY_PORT: int

    PARSER_SERVICE_PROTOCOL: str
    PARSER_SERVICE_HOST: str
    PARSER_SERVICE_PORT: int

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

    @property
    def parser_service_url(self) -> str:
        return f"{self.PARSER_SERVICE_PROTOCOL}://{self.PARSER_SERVICE_HOST}:{self.PARSER_SERVICE_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
