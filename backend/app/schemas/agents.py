from pydantic import BaseModel
from typing import Optional


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
    filepath: Optional[str]
    # Register Model
    modelProvider: str
    repoID: str
    modelFormat: str
    modelName: str
    token: str
