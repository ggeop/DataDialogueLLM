from app.agents.text_to_sql_agent import TextToSQLAgent
from app.clients.db import DatabaseClient
from app.llm import LanguageModel
from app.llm.model_type import ModelType
from app.schemas import (
    SQLResponse,
    GeneralResponse,
    DialogueResult

)


class DataDialogueAgent:
    def __init__(
        self,
        database: DatabaseClient,
        model: LanguageModel,
    ):
        self.model = model
        self.database = database
        self.is_sql_relevant = self.database and (model.model_type == ModelType.SQL.value)
        if self.is_sql_relevant:
            self.sql_agent = TextToSQLAgent(model, database)
        else:
            self.sql_agent = None

    def generate(self, prompt: str) -> DialogueResult:

        if self.sql_agent:
            sql_agent_name = self.sql_agent.__class__.__name__
            sql, results, error = self.sql_agent.generate(prompt)
            response = SQLResponse(sql=sql, results=results, error=error)
            agent = sql_agent_name
        else:
            general_agent_name = self.model.__class__.__name__
            general_response = self.model.generate(prompt)
            response = GeneralResponse(response=general_response)
            agent = general_agent_name

        return DialogueResult(
            user_prompt=prompt,
            agent=agent,
            response=response,
            is_sql_response=bool(self.is_sql_relevant)
        )
