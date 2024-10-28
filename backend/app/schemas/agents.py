from app.schemas.base import BaseModel


class RegisterAgent(BaseModel):
    # General
    agentType: str
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
