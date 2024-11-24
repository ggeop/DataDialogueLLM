from typing import Any, Optional, Union, List,  Generic, TypeVar

from pydantic import BaseModel
from dataclasses import field

# Generic type for data
T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response model with status and message"""
    status: str = "success"
    message: str


class DataResponse(BaseResponse, Generic[T]):
    """Response model with data field"""
    data: Optional[T] = None


class PaginatedResponse(DataResponse[List[T]], Generic[T]):
    """Response model for paginated results"""
    total: int
    page: int
    size: int
    pages: int


# Agent-specific responses
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
    

class AgentList(BaseModel):
    """List of agents model"""
    agents: List[str]


# Error responses
class ErrorDetail(BaseModel):
    """Detailed error information"""
    code: str
    message: str
    field: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    status: str = "error"
    message: str
    details: Optional[List[ErrorDetail]] = None
