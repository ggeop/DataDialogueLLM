from enum import Enum

from .base import ModelLoader
from .google.loader import GoogleAILoader
from .llama.loader import LlamaGGUFLoader
from .openai.loader import OpenAILoader


class SupportedModelSources(Enum):
    GOOGLE = "google"
    GGUF = "gguf"
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"


__all__ = [ModelLoader, GoogleAILoader, LlamaGGUFLoader, OpenAILoader, SupportedModelSources]
