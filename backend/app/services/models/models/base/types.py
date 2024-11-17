from dataclasses import dataclass
from typing import Optional, List


@dataclass
class CompletionResponse:
    """Standardized response format for model completions"""

    text: str
    finish_reason: Optional[str] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


@dataclass
class EmbeddingResponse:
    """Standardized response format for embeddings"""

    embedding: List[float]
    model_name: str
