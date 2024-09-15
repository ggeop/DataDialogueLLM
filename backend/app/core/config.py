from pydantic_settings import BaseSettings
from typing import List
import os

MODEL_FILE = os.getenv('MODEL_FILE')
if not MODEL_FILE:
    raise ValueError("MODEL_FILE environment variable is not set or is empty")

MODEL_LOCAL_DIR = os.getenv('MODEL_LOCAL_DIR')
if not MODEL_LOCAL_DIR:
    raise ValueError("MODEL_LOCAL_DIR environment variable is not set or is empty")


class Settings(BaseSettings):
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    MODEL_PATH: str = os.path.join(MODEL_LOCAL_DIR, MODEL_FILE)

    # Generation settings
    MAX_TOKENS: int = 3000
    STOP_SEQUENCES: List[str] = ["Human:", "\n\n"]

    class Config:
        env_file = ".env"


settings = Settings()
