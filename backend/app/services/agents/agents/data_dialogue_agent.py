from app.services.agents.agents.text_to_sql_agent import TextToSQLAgent
from app.clients.db import DatabaseClient
from app.core.model_type import AgentType
from app.schemas import SQLResponse, GeneralResponse, DialogueResult


class DataDialogueAgent:
    def __init__(
        self, database: DatabaseClient, model, model_type: str, agent_name: str
    ):
        self.model = model
        self.database = database
        self.model_type = model_type
        self.name = agent_name
        self.is_sql_relevant = self.database and (
            self.model_type == AgentType.SQL.value
        )
        if self.is_sql_relevant:
            self.sql_agent = TextToSQLAgent(model, database)
        else:
            self.sql_agent = None

    def generate(self, prompt: str) -> DialogueResult:
        if self.sql_agent:
            sql_agent_name = self.sql_agent.__class__.__name__
            sql, data, column_names, error = self.sql_agent.generate(prompt)
            response = SQLResponse(
                sql=sql, results=data, column_names=column_names, error=error
            )
            agent = sql_agent_name
        else:
            prompt = f"Q: {prompt} A: "
            model_response = self.model.complete(
                prompt,
                max_tokens=200,
                temperature=0.6,
                stop=["\n"],
            )
            general_response = model_response.text.strip()
            response = GeneralResponse(response=general_response)
            agent = self.name

        return DialogueResult(
            user_prompt=prompt,
            agent=agent,
            response=response,
            is_sql_response=bool(self.is_sql_relevant),
        )
