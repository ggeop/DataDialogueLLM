import logging
from typing import Dict, List

from app.clients.db import PostgresClient
from app.schemas import RegisterAgent
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.services.model_management import ModelManager
from app.core.config import settings
from app.core.model_type import ModelType

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
            source="huggingface",
            repo_id=register_params.repoID,
            model_name=register_params.modelName
        )
        model = self.model_manager.load_model(
            source="huggingface",
            repo_id=register_params.repoID,
            model_name=register_params.modelName,
            model_type="gguf",
            n_ctx=3000,
            verbose=False
        )
        sql_agent = DataDialogueAgent(
            database=db,
            model=model,
            model_type=ModelType.SQL.value
        )
        self.registered_agents[sql_agent.name] = sql_agent

    def _initialize_agents(self):
        # =============================
        # General Agent Setup
        # =============================
        self.model_manager.download_model(
            source=settings.DEFAULT_GENERAL_LLM["source"],
            repo_id=settings.DEFAULT_GENERAL_LLM["repo_id"],
            model_name=settings.DEFAULT_GENERAL_LLM["model_name"])

        general_model = self.model_manager.load_model(
            source=settings.DEFAULT_GENERAL_LLM["source"],
            repo_id=settings.DEFAULT_GENERAL_LLM["repo_id"],
            model_name=settings.DEFAULT_GENERAL_LLM["model_name"],
            model_type="gguf",
            verbose=False
        )

        general_agent = DataDialogueAgent(
            database=None,
            model=general_model,
            model_type=ModelType.GENERAL.value
        )
        self.registered_agents[general_agent.name] = general_agent

    def _is_registered(self, model) -> bool:
        return model in self.registered_agents


data_dialogue_service = DataDialogueService()
