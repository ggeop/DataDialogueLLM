from abc import ABC, abstractmethod
from typing import List
from llama_cpp import Llama


class LanguageModel(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int, stop: List[str], temperature=0.8) -> str:
        pass


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


class SQLLlamaModel(LanguageModel):
    def __init__(self, model_path: str):
        self.llm = Llama(
            model_path=model_path,
            verbose=False
        )

    def generate(self, prompt: str, max_tokens: int=100, stop: List[str]=[], temperature: float=0) -> str:
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop,
            echo=False
        )
        return response['choices'][0]['text'].strip()