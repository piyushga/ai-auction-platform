from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    OPENAI_API_KEY: str

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()