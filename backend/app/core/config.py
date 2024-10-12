from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Generation settings
    MAX_TOKENS: int = 3000
    STOP_SEQUENCES: List[str] = ["Human:", "\n\n"]

    class Config:
        env_file = ".env"


settings = Settings()
