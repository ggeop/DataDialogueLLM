from typing import Any, Optional, Union
from pydantic import BaseModel

from app.models.database import Database
from app.models.language_model import LanguageModel
from app.agents.text_to_sql_agent import TextToSQLAgent
from app.agents.question_relevance_agent import QuestionRelevanceAgent
from app.core.config import settings


class SQLResponse(BaseModel):
    sql: str
    results: Any
    error: Optional[str] = None


class GeneralResponse(BaseModel):
    response: str


class DialogueResult(BaseModel):
    user_prompt: str
    agent: str
    response: Union[SQLResponse, GeneralResponse]
    is_sql_response: bool


class DataDialogueAgent:
    def __init__(
        self,
        database: Database,
        sql_model: LanguageModel,
        general_model: LanguageModel,
        relevance_threshold: float = 0.6
    ):
        self.database = database
        if database:
            self.relevance_checker = QuestionRelevanceAgent(
                db_tables=database.get_tablenames(),
                threshold=relevance_threshold,
                model_path=settings.MODEL_PATH
            )
        else:
            self.relevance_checker = None
        self.sql_agent = TextToSQLAgent(sql_model, database)
        self.general_model = general_model

    def generate(self, prompt: str) -> DialogueResult:
        if self.relevance_checker:
            is_sql_relevant, _ = self.relevance_checker.check_relevance(prompt)
        else:
            is_sql_relevant, _ = False, None

        if is_sql_relevant:
            sql_agent_name = self.sql_agent.__class__.__name__
            sql, results, error = self.sql_agent.generate(prompt)
            response = SQLResponse(sql=sql, results=results, error=error)
            agent = sql_agent_name
        else:
            general_agent_name = self.general_model.__class__.__name__
            general_response = self.general_model.generate(prompt)
            response = GeneralResponse(response=general_response)
            agent = general_agent_name

        return DialogueResult(
            user_prompt=prompt,
            agent=agent,
            response=response,
            is_sql_response=is_sql_relevant
        )
