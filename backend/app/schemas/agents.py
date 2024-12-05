from pydantic import BaseModel


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
    modelProvider: str
    repoID: str
    modelFormat: str
    modelName: str
    token: str
