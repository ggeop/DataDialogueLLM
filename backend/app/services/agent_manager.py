import logging
from typing import Dict, List

from app.clients.db import PostgresClient
from app.schemas import RegisterAgent
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.services.model_management import ModelManager
from app.core.config import settings
from app.core.model_type import AgentType

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentManagerService:
    """
    A service for managing model agents in a dialogue system.

    This service is responsible for registering, retrieving, and deleting model agents.
    It supports different types of models and databases, and manages the lifecycle of these agents.

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
        self._initialize_agents()

    def get_agents(self) -> List[str]:
        """
        Get a list of all registered agent names.

        Returns:
            List[str]: A list of strings representing the names of all registered agents.

        Example:
            agent_names = service.get_agents()
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
            raise ValueError(f"'{agent_name}' is not a valid agent. Registered agents are: {valid_agents}")
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
            raise ValueError(f"Cannot delete '{agent_name}'. Registered agents are: {valid_agents}")
        del self.registered_agents[agent_name]
        logger.info(f"Agent '{agent_name}' has been successfully deleted.")

    def register_agent(self, register_params: RegisterAgent):
        """
        Register a new agent based on the provided parameters.

        This method validates the model type, configures the database (if applicable),
        loads the model, and creates a new DataDialogueAgent instance.

        Args:
            register_params (RegisterAgent): Parameters for registering the agent.

        Raises:
            ValueError: If the model type is not supported or the source type is invalid.

        Example:
            params = RegisterAgent(
                agentType="SQL",
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
        database = self._configure_database(register_params)
        model = self._load_model(register_params)

        agent = DataDialogueAgent(
            database=database,
            model=model,
            model_type=register_params.agentType
        )
        self.registered_agents[agent.name] = agent
        logger.info(f"Agent '{agent.name}' has been successfully registered.")

    def _initialize_agents(self):
        """
        Initialize the default general agent.

        This private method is called during the service initialization to set up
        any default agents, such as a general-purpose dialogue agent.

        Note:
            This method is not intended to be called directly.
        """
        general_model = self._load_default_model()
        general_agent = DataDialogueAgent(
            database=None,
            model=general_model,
            model_type=AgentType.GENERAL.value
        )
        self.registered_agents[general_agent.name] = general_agent
        logger.info(f"Default general agent '{general_agent.name}' has been initialized.")

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
            raise ValueError(f"'{model_type}' is not a valid model type. Supported types are: {', '.join(supported_model_types)}")

    def _configure_database(self, register_params: RegisterAgent):
        """
        Configure and return the database client based on the registration parameters.

        Args:
            register_params (RegisterAgent): The registration parameters containing database configuration.

        Returns:
            Optional[PostgresClient]: A configured database client, or None if no database is required.

        Raises:
            ValueError: If an unsupported source type is specified.

        Note:
            This is a private method intended for internal use only.
        """
        if register_params.agentType == AgentType.SQL.value:
            if register_params.sourceType == 'postgresql':
                db = PostgresClient(
                    dbname=register_params.dbname,
                    user=register_params.username,
                    password=register_params.password,
                    host=register_params.host,
                    port=register_params.port
                )
                db.test_connection()
                return db
            else:
                raise ValueError(f"Unsupported source type: {register_params.sourceType}")
        return None

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
        return self.model_manager.load_model(
            source=register_params.modelSource,
            repo_id=register_params.repoID,
            model_name=register_params.modelName,
            model_format=register_params.modelFormat,
            n_ctx=3000,
            verbose=False
        )

    def _load_default_model(self):
        """
        Load and return the default general model.

        Returns:
            Any: The loaded default model object.

        Note:
            This is a private method intended for internal use only.
        """
        return self.model_manager.load_model(
            source=settings.DEFAULT_GENERAL_LLM["source"],
            repo_id=settings.DEFAULT_GENERAL_LLM["repo_id"],
            model_name=settings.DEFAULT_GENERAL_LLM["model_name"],
            model_format=settings.DEFAULT_GENERAL_LLM["model_format"],
            verbose=False
        )


agent_manager_service = AgentManagerService()
