from app.schemas.base import BaseModel


class DatabaseCreationResponse(BaseModel):
    message: str


class RegisterSource(BaseModel):
    dbname: str
    sourceType: str
    username: str
    password: str
    host: str
    port: str
