import logging
from typing import Dict, List

from app.clients.db import PostgresClient
from app.llm import SQLLlama31Model, GeneralLlama31Model
from app.schemas import RegisterSource
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.services.database import create_examples_database
from app.core.config import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DataDialogueService:
    def __init__(self):
        self.registered_agents: Dict[str, DataDialogueAgent] = {}
        self._initialize_agents()  # TODO: TMP Solution, until try-on feature will be created

    def get_agents(self) -> List[str]:
        return list(self.registered_agents.keys())

    def get_agent(self, model: str) -> DataDialogueAgent:
        if not self._is_registered(model):
            message = f"`{model}` is not a valid model. Valid registered models are {list(self.registered_agents.keys())}"
            logger.error(message)
            raise ValueError(message)
        return self.registered_agents[model]

    def delete_agent(self, model: str) -> None:
        if not self._is_registered(model):
            message = f"`{model}` is not deleted. `{model}` is not a valid model. Valid registered models are {list(self.registered_agents.keys())}"
            logger.error(message)
            raise ValueError(message)
        del self.registered_agents[model]
        logger.info(f"{model} is deleted successful!")

    def register_source(self, register_params: RegisterSource):
        logger.info(f"Try to register with params: {register_params}")
        if register_params.sourceType == 'postgresql':
            db = PostgresClient(
                dbname=register_params.dbname,
                user=register_params.username,
                password=register_params.password,
                host=register_params.host,
                port=register_params.port
            )
            db.test_connection()
            logger.info(db.get_tablenames())
            model = SQLLlama31Model(settings.MODEL_PATH)
            self.registered_agents[model.alias] = DataDialogueAgent(
                database=db,
                model=model
            )

    def _initialize_agents(self):
        sql_model = SQLLlama31Model(settings.MODEL_PATH)
        database_agent = DataDialogueAgent(
            database=create_examples_database(),
            model=sql_model,
        )
        self.registered_agents[sql_model.alias] = database_agent

        general_model = GeneralLlama31Model(settings.MODEL_PATH)
        general_agent = DataDialogueAgent(
            database=None,
            model=general_model,
        )
        self.registered_agents[general_model.alias] = general_agent

    def _is_registered(self, model) -> bool:
        return model in self.registered_agents


data_dialogue_service = DataDialogueService()
