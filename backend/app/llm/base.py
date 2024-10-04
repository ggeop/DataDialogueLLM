from abc import ABC, abstractmethod
from typing import List


class LanguageModel(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int, stop: List[str], temperature=0.8) -> str:
        pass
