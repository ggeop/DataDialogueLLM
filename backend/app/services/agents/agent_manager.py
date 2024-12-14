import logging
from typing import Dict, List

from app.schemas import RegisterAgent
from app.services.agents.agents.data_dialogue_agent import DataDialogueAgent
from app.services.models import ModelManager
from app.core.config import settings
from app.core.model_type import AgentType
from app.services.models.downloader import HuggingFaceDownloader
from app.services.models.models import (
    GoogleAILoader,
    OpenAILoader,
    AnthropicLoader,
    LlamaGGUFLoader,
    ModelProvider,
    ModelFormat,
)
from app.services.sources.db import PostgresClient, MySQLClient, MongoDBClient
from app.services.sources.cloud import DatabaseClient
from app.services.sources.config import SourceType
from app.services.sources.files.csv_client import CSVClient


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentManagerService:
    """
    A service for managing model agents in a dialogue system.

    This service is responsible for registering, retrieving, and deleting model agents.
    It supports different types of models and sources, and manages the lifecycle of these agents.

    Attributes:
        registered_agents (Dict[str, DataDialogueAgent]): A dictionary of registered agents.
        model_manager (ModelManager): An instance of ModelManager for handling model operations.

    Example:
        service = AgentManagerService()
        service.register_agent(register_params)
        agent = service.get_agent("agent_name")
        service.delete_agent("agent_name")
    """

    def __init__(self):
        """
        Initialize the AgentManagerService.

        This constructor sets up the registered_agents dictionary, initializes the ModelManager,
        and calls the _initialize_agents method to set up any default agents.
        """
        self.registered_agents: Dict[str, DataDialogueAgent] = {}
        self.model_manager = ModelManager(base_path=settings.MODELS_BASE_PATH)

    def register_agent(self, register_params: RegisterAgent):
        """
        Register a new agent based on the provided parameters.

        This method validates the model type, configures the source (if applicable),
        loads the model, and creates a new DataDialogueAgent instance.

        Args:
            register_params (RegisterAgent): Parameters for registering the agent.

        Raises:
            ValueError: If the model type is not supported or the source type is invalid.

        Example:
            params = RegisterAgent(
                agentType="Contextual",
                sourceType="postgresql",
                dbname="mydb",
                username="user",
                password="pass",
                host="localhost",
                port="5432",
                repoID="myrepo",
                modelName="mymodel"
            )
            try:
                service.register_agent(params)
                print("Agent successfully registered.")
            except ValueError as e:
                print(f"Error: {e}")
        """
        logger.info(f"Attempting to register agent with params: {register_params}")

        self._validate_model_type(register_params.agentType)

        source_client = None
        if register_params.agentType == AgentType.CONTEXTUAL.value:
            source_client = self._configure_source(register_params)

        # NOTE: The naming convention should be consistent with frontend (e.g FormsHandling.js)
        agent_name = f"({register_params.agentType}) {register_params.modelName}"

        agent = DataDialogueAgent(
            source_client=source_client,
            model=self._load_model(register_params),
            model_type=register_params.agentType,
            agent_name=agent_name,
        )
        self.registered_agents[agent.name] = agent
        logger.info(f"Agent '{agent.name}' has been successfully registered.")

    def get_agents(self) -> Dict:
        """
        Get a dictionary of all registered agent.

        Returns:
            Dict: A dict of all registered agents.
        """
        return self.registered_agents

    def get_agent_names(self) -> List[str]:
        """
        Get a list of all registered agent names.

        Returns:
            List[str]: A list of strings representing the names of all registered agents.

        Example:
            agent_names = service.get_agent_names()
            print(f"Registered agents: {', '.join(agent_names)}")
        """
        return list(self.registered_agents.keys())

    def get_agent(self, agent_name: str) -> DataDialogueAgent:
        """
        Retrieve a registered agent by its name.

        Args:
            agent_name (str): The name of the agent to retrieve.

        Returns:
            DataDialogueAgent: The requested agent instance.

        Raises:
            ValueError: If the specified agent_name is not registered.

        Example:
            try:
                agent = service.get_agent("sql_agent")
                # Use the agent...
            except ValueError as e:
                print(f"Error: {e}")
        """
        if not self._is_registered(agent_name):
            valid_agents = ", ".join(self.registered_agents.keys())
            raise ValueError(
                f"'{agent_name}' is not a valid agent. Registered agents are: {valid_agents}"
            )
        return self.registered_agents[agent_name]

    def delete_agent(self, agent_name: str) -> None:
        """
        Delete a registered agent.

        Args:
            agent_name (str): The name of the agent to delete.

        Raises:
            ValueError: If the specified agent_name is not registered.

        Example:
            try:
                service.delete_agent("outdated_agent")
                print("Agent successfully deleted.")
            except ValueError as e:
                print(f"Error: {e}")
        """
        if not self._is_registered(agent_name):
            valid_agents = ", ".join(self.registered_agents.keys())
            raise ValueError(
                f"Cannot delete '{agent_name}'. Registered agents are: {valid_agents}"
            )
        del self.registered_agents[agent_name]
        logger.info(f"Agent '{agent_name}' has been successfully deleted.")

    def _is_registered(self, agent_name: str) -> bool:
        """
        Check if an agent is registered.

        Args:
            agent_name (str): The name of the agent to check.

        Returns:
            bool: True if the agent is registered, False otherwise.

        Note:
            This is a private method intended for internal use only.
        """
        return agent_name in self.registered_agents

    def _validate_model_type(self, model_type: str):
        """
        Validate the given model type.

        Args:
            model_type (str): The model type to validate.

        Raises:
            ValueError: If the model type is not supported.

        Note:
            This is a private method intended for internal use only.
        """
        supported_model_types = AgentType.values()
        if model_type not in supported_model_types:
            raise ValueError(
                f"'{model_type}' is not a valid model type. Supported types are: {', '.join(supported_model_types)}"
            )

    def _configure_source(self, register_params: RegisterAgent):
        """
        Configure and return the source client based on the registration parameters.

        Args:
            register_params (RegisterAgent): The registration parameters containing source configuration.

        Returns:
            Optional[PostgresClient]: A configured source client, or None if no source is required.

        Raises:
            ValueError: If an unsupported source type is specified.

        Note:
            This is a private method intended for internal use only.
        """
        if register_params.sourceType == SourceType.POSTGRESQL.value:
            client = PostgresClient(
                dbname=register_params.dbname,
                user=register_params.username,
                password=register_params.password,
                host=register_params.host,
                port=register_params.port,
            )
            client.test_connection()
            return client
        elif register_params.sourceType == SourceType.MYSQL.value:
            client = MySQLClient(
                dbname=register_params.dbname,
                user=register_params.username,
                password=register_params.password,
                host=register_params.host,
                port=register_params.port,
            )
            client.test_connection()
            return client
        elif register_params.sourceType == SourceType.MONGODB.value:
            client = MongoDBClient(
                dbname=register_params.dbname,
                user=register_params.username,
                password=register_params.password,
                host=register_params.host,
                port=register_params.port,
            )
            client.test_connection()
            return client
        elif register_params.sourceType == SourceType.DATABRICKS.value:
            client = DatabaseClient(
                dbname=register_params.dbname,
                user=register_params.username,
                password=register_params.password,
                host=register_params.host,
                port=register_params.port,
            )
            client.test_connection()
            return client
        elif register_params.sourceType == SourceType.CSV.value:
            client = CSVClient(path=register_params.filepath)
            return client
        else:
            raise ValueError(f"Unsupported source type: {register_params.sourceType}")

    def _load_model(self, register_params: RegisterAgent):
        """
        Load and return the model based on the registration parameters.

        Args:
            register_params (RegisterAgent): The registration parameters containing model information.

        Returns:
            Any: The loaded model object.

        Note:
            This is a private method intended for internal use only.
        """

        # --------------------------------------------
        # Register model loader + downloaders
        # --------------------------------------------
        if register_params.modelProvider == ModelProvider.GOOGLE.value:
            self.model_manager.register_loader(
                ModelProvider.GOOGLE.value,
                GoogleAILoader(api_key=register_params.token),
            )
        elif register_params.modelProvider == ModelProvider.OPENAI.value:
            self.model_manager.register_loader(
                ModelProvider.OPENAI.value, OpenAILoader(api_key=register_params.token)
            )
        elif register_params.modelProvider == ModelProvider.ANTHROPIC.value:
            self.model_manager.register_loader(
                ModelProvider.ANTHROPIC.value,
                AnthropicLoader(api_key=register_params.token),
            )
        elif register_params.modelProvider == ModelProvider.HUGGINGFACE.value:
            if register_params.modelFormat == ModelFormat.GGUF.value:
                self.model_manager.register_loader(
                    ModelProvider.HUGGINGFACE.value, LlamaGGUFLoader()
                )
                self.model_manager.register_downloader(
                    ModelProvider.HUGGINGFACE.value,
                    HuggingFaceDownloader(token=register_params.token),
                )
            else:
                raise Exception(
                    f"Not known `modelFormat`: {register_params.modelFormat}"
                )
        else:
            raise Exception(
                f"Not known `modelProvider`: {register_params.modelProvider}"
            )

        # --------------------------------------------
        # Load Model
        # --------------------------------------------
        model = self.model_manager.load_model(
            source=register_params.modelProvider,
            repo_id=register_params.repoID,
            model_name=register_params.modelName,
            model_format=register_params.modelFormat,
        )

        return model


agent_manager_service = AgentManagerService()
