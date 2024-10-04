from pydantic import BaseModel
from typing import Any, Optional, Union


class Query(BaseModel):
    text: str


class DatabaseCreationResponse(BaseModel):
    message: str


class RegisterSource(BaseModel):
    dbname: str
    sourceType: str
    username: str
    password: str
    host: str
    port: str


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
