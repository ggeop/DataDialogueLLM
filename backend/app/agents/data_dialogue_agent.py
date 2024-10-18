from app.agents.text_to_sql_agent import TextToSQLAgent
from app.clients.db import DatabaseClient
from app.core.model_type import ModelType
from app.schemas import (
    SQLResponse,
    GeneralResponse,
    DialogueResult

)


class DataDialogueAgent:
    def __init__(
        self,
        database: DatabaseClient,
        model,
        model_type: str
    ):
        self.model = model
        self.database = database
        self.model_type = model_type
        self.is_sql_relevant = self.database and (self.model_type == ModelType.SQL.value)
        if self.is_sql_relevant:
            self.sql_agent = TextToSQLAgent(model, database)
        else:
            self.sql_agent = None

        self._model_name = model.metadata.get('general.name')
        self.name = f"({self.model_type}) {self._model_name}"

    def generate(self, prompt: str) -> DialogueResult:
        agent_name = self.model.__class__.__name__

        if self.sql_agent:
            sql_agent_name = self.sql_agent.__class__.__name__
            sql, results, error = self.sql_agent.generate(prompt)
            response = SQLResponse(sql=sql, results=results, error=error)
            agent = sql_agent_name
        else:
            prompt = f"Q: {prompt} A: "
            model_response = self.model(
                prompt,
                max_tokens=200,
                temperature=0.6,
                stop=["\n"],
                echo=False)
            general_response = model_response['choices'][0]['text'].strip()
            response = GeneralResponse(response=general_response)
            agent = agent_name

        return DialogueResult(
            user_prompt=prompt,
            agent=agent,
            response=response,
            is_sql_response=bool(self.is_sql_relevant)
        )