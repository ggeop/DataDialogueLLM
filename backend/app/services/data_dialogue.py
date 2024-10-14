import logging
from typing import Dict, List

from app.clients.db import PostgresClient
from app.llm import SQLLlama31Model, GeneralLlama31Model
from app.schemas import RegisterAgent
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.llm.model_manager import ModelManager
from app.core.config import settings
from app.llm.model_type import ModelType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class DataDialogueService:
    def __init__(self):
        self.registered_agents: Dict[str, DataDialogueAgent] = {}
        self.model_manager = ModelManager(base_path=settings.MODELS_BASE_PATH)
        self._initialize_agents()

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

    def register_agent(self, register_params: RegisterAgent):
        logger.info(f"Try to register with params: {register_params}")

        supported_model_types = ModelType.values()
        if register_params.modelType not in supported_model_types:
            raise Exception(f"{register_params.modelType} is not a valid modelType value. Supported values are: {supported_model_types}")

        # =============================
        # Configure External Source
        # =============================
        if register_params.modelType == ModelType.SQL.value:
            if register_params.sourceType == 'postgresql':
                db = PostgresClient(
                    dbname=register_params.dbname,
                    user=register_params.username,
                    password=register_params.password,
                    host=register_params.host,
                    port=register_params.port
                )
                db.test_connection()
            else:
                raise Exception(f"Not supported {register_params.sourceType} source type")
        elif register_params.modelType == ModelType.GENERAL.value:
            db = None

        # =============================
        # Configure LLM Model
        # =============================
        self.model_manager.download_model(
            source="huggingface",  # TODO: Support only HuggingFace repository
            repo_id=register_params.repoID,
            model_name=register_params.modelName
        )
        self.sql_model_path = self.model_manager.get_model_path(f'{register_params.repoID}/{register_params.modelName}')

        model = SQLLlama31Model(self.sql_model_path)
        self.registered_agents[model.alias] = DataDialogueAgent(
            database=db,
            model=model
        )

    def _initialize_agents(self):
        # =============================
        # General Agent Setup
        # =============================
        self.model_manager.download_model(
            source=settings.DEFAULT_GENERAL_LLM["source"],
            repo_id=settings.DEFAULT_GENERAL_LLM["repo_id"],
            model_name=settings.DEFAULT_GENERAL_LLM["model_name"])

        self.general_model_path = self.model_manager.get_model_path(f'{settings.DEFAULT_GENERAL_LLM["repo_id"]}/{settings.DEFAULT_GENERAL_LLM["model_name"]}')

        general_model = GeneralLlama31Model(self.general_model_path)
        general_agent = DataDialogueAgent(
            database=None,
            model=general_model,
        )
        self.registered_agents[general_model.alias] = general_agent

    def _is_registered(self, model) -> bool:
        return model in self.registered_agents


data_dialogue_service = DataDialogueService()
