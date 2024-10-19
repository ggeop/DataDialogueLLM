from app.schemas.base import BaseModel


class DatabaseCreationResponse(BaseModel):
    message: str


class RegisterAgent(BaseModel):

    # General
    modelType: str

    # Register Source
    dbname: str
    sourceType: str
    username: str
    password: str
    host: str
    port: str

    # Register Model
    modelSource: str
    repoID: str
    modelFormat: str
    modelName: str
    token: str
