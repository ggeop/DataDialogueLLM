
from typing import List

from llama_cpp import Llama

from app.llm.base import LanguageModel
from app.llm.model_type import ModelType


class GeneralLlama31Model(LanguageModel):
    def __init__(self, model_path: str):
        self.model_type = ModelType.GENERAL.value
        self.model = "LLAMA"
        self.version = "3.1"
        self.alias = f"{self.model_type} ({self.model} {self.version})"
        self.llm = Llama(
            model_path=model_path,
            verbose=False
        )

    def generate(self, prompt: str, max_tokens: int=100, stop: List=["\n"], temperature: float=0.3) -> str:
        prompt = f"Q: {prompt} A: "
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop,
            echo=False)
        return response['choices'][0]['text'].strip()
