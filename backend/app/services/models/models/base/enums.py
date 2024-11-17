from enum import Enum


class TaskType(Enum):
    """Enum for different types of models"""
    COMPLETION = "completion"
    CHAT = "chat"
    EMBEDDING = "embedding"
