from abc import ABC, abstractmethod
from typing import List


class LanguageModel(ABC):
    def __init__(self):
        self.model_type = None
        self.model = None
        self.version = None
        self.alias = None

    @abstractmethod
    def generate(self, prompt: str, max_tokens: int, stop: List[str], temperature=0.8) -> str:
        pass
