from typing import Any, Optional, Union, List

from pydantic import BaseModel
from dataclasses import field


class SQLResponse(BaseModel):
    sql: str
    results: Any
    column_names: List[str] = field(default_factory=list)
    error: Optional[str] = None


class GeneralResponse(BaseModel):
    response: str


class DialogueResult(BaseModel):
    user_prompt: str
    agent: str
    response: Union[SQLResponse, GeneralResponse]
    is_sql_response: bool
