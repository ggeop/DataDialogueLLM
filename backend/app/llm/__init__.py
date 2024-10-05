from app.llm.base import LanguageModel
from app.llm.general.llama_3_1 import GeneralLlama31Model
from app.llm.sql.llama_3_1 import SQLLlama31Model

__all__ = [
    LanguageModel,
    GeneralLlama31Model,
    SQLLlama31Model
]

registry = [
    GeneralLlama31Model,
    SQLLlama31Model
]
