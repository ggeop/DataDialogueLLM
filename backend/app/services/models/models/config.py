from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class ModelProvider(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HUGGINGFACE = "huggingface"


class ModelFormat(str, Enum):
    GGUF = "gguf"


class ModelOption(BaseModel):
    value: Optional[str] = None
    label: Optional[str] = None
    suggested: Optional[bool] = False
    size: Optional[str] = None
    repo_id: Optional[str] = None
    has_token: Optional[bool] = None
    # Nested options for repo variants (e.g for HuggingFace models)
    variants: Optional[List["ModelOption"]] = None


class ModelConfig(BaseModel):
    source_id: ModelProvider
    display_name: str
    logo_path: str
    suggested: bool = False
    is_local: bool = False
    has_token: Optional[bool] = None
    options: List[ModelOption]


ModelOption.model_rebuild()
