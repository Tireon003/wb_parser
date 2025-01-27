from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    BOT_TOKEN: str

    API_GATEWAY_HOST: str
    API_GATEWAY_PORT: int
    API_GATEWAY_PROTOCOL: str

    LOG_LEVEL: str
    LOG_FORMAT: str

    @property
    def api_gateway_url(self) -> str:
        return f"{self.API_GATEWAY_PROTOCOL}://{self.API_GATEWAY_HOST}:{self.API_GATEWAY_PORT}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
