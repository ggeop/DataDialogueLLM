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
        "repo_id": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
        "model_name": "Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
    }

    class Config:
        env_file = ".env"


settings = Settings()
