from pydantic import BaseModel


class Query(BaseModel):
    text: str
    agent: str
