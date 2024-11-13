from pydantic import BaseModel


class DatabaseCreationResponse(BaseModel):
    message: str
