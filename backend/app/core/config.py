from pydantic_settings import BaseSettings
from typing import List, Dict


class Settings(BaseSettings):
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Generation settings
    MAX_TOKENS: int = 3000
    STOP_SEQUENCES: List[str] = ["Human:", "\n\n"]

    MODELS_BASE_PATH: str = "/data/models"

    DEFAULT_GENERAL_LLM: Dict[str, str] = {
        "source": "huggingface",
        "repo_id": "mradermacher/Hrida-T2SQL-3B-128k-V0.1-GGUF",
        "model_name": "Hrida-T2SQL-3B-128k-V0.1.Q4_K_S.gguf"
    }

    class Config:
        env_file = ".env"


settings = Settings()
