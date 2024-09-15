from llama_cpp import Llama
from app.core.config import settings
import os


class LLMService:
    def __init__(self):
        if not os.path.exists(settings.MODEL_PATH):
            raise FileNotFoundError(f"Model file {settings.MODEL_PATH} doesn't exist")
        self.model = Llama(
            model_path=settings.MODEL_PATH,
            chat_format="llama-2"
        )

    def generate_response(self, prompt: str) -> str:
        response = self.model(
            prompt,
            max_tokens=settings.MAX_TOKENS,
            stop=settings.STOP_SEQUENCES,
            echo=True
        )
        return response['choices'][0]['text'].split("Assistant:")[-1].strip()

llm_service = LLMService()
