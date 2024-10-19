from typing import Any, Optional, Union

from app.schemas.base import BaseModel


class SQLResponse(BaseModel):
    sql: str
    results: Any
    error: Optional[str] = None


class GeneralResponse(BaseModel):
    response: str


class DialogueResult(BaseModel):
    user_prompt: str
    agent: str
    response: Union[SQLResponse, GeneralResponse]
    is_sql_response: bool
