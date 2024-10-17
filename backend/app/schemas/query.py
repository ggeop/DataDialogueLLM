from app.schemas.base import BaseModel


class Query(BaseModel):
    text: str
    agent: str
