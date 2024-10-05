import logging

from app.clients.db import PostgresClient
from app.llm import registry, SQLLlama31Model, GeneralLlama31Model
from app.llm.model_type import ModelType
from app.schemas import RegisterSource
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.services.database import create_examples_database
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


registered_agents = {}

# ===================
# Initialize Agents
# ===================
model = SQLLlama31Model(settings.MODEL_PATH)
database_agent = DataDialogueAgent(
    database=create_examples_database(),
    model=model,
)
registered_agents[model.alias] = database_agent

model = GeneralLlama31Model(settings.MODEL_PATH)
general_agent = DataDialogueAgent(
    database=None,
    model=model,
)
registered_agents[model.alias] = general_agent


def get_data_dialogue_agent(model):
    global registered_agents
    if model not in registered_agents:
        message = f"`{model}` is not a valid model. Valid registered models are {list(registered_agents.keys())}"
        logger.error(message)
        raise Exception(message)
    return registered_agents[model]


def update_data_dialogue_service(register_params: RegisterSource):
    global data_dialogue_service
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
        logger.info(db.get_schema())
        model = SQLLlama31Model(settings.MODEL_PATH)
        registered_agents[model.alias] = DataDialogueAgent(
            database=db,
            model=model
        )
