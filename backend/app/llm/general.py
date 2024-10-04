
from typing import List

from llama_cpp import Llama

from app.llm.base import LanguageModel


class GeneralLlamaModel(LanguageModel):
    def __init__(self, model_path: str):
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
