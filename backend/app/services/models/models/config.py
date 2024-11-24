from enum import Enum
from pydantic import BaseModel
from typing import List, Optional


class ModelSource(str, Enum):
    GOOGLE = "google"
    OPENAI = "openai"
    HUGGINGFACE = "huggingface"


class ModelFormat(str, Enum):
    GGUF = "gguf"


class ModelOption(BaseModel):
    value: str
    label: str
    suggested: bool = False
    size: Optional[str] = None
    repo_id: Optional[str] = None


class ModelConfig(BaseModel):
    source_id: ModelSource
    display_name: str
    logo_path: str
    suggested: bool = False
    is_local: bool = False
    options: List[ModelOption]
