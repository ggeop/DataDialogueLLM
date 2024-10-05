
from typing import List

from llama_cpp import Llama

from app.llm.base import LanguageModel


class SQLLlamaModel(LanguageModel):
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            verbose=False,
            n_ctx=1024
        )

    def generate(self, prompt: str, max_tokens: int=300, stop: List[str]=[], temperature: float=0) -> str:
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop,
            echo=False
        )
        return response['choices'][0]['text'].strip()
