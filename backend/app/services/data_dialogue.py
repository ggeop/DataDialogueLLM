import logging

from app.clients.db import PostgresClient
from app.llm import SQLModel, GeneralModel
from app.schemas import RegisterSource
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.services.database import create_examples_database
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Service Initialization
database = create_examples_database()
data_dialogue_service = DataDialogueAgent(
    database=database,
    sql_model=SQLModel(settings.MODEL_PATH),
    general_model=GeneralModel(settings.MODEL_PATH)
)


def get_data_dialogue_service():
    global data_dialogue_service
    return data_dialogue_service


def update_data_dialogue_service(register_params: RegisterSource):
    global data_dialogue_service
    logger.info(f"Try to register with params: {register_params}")
    db = PostgresClient(
        dbname=register_params.dbname,
        user=register_params.username,
        password=register_params.password,
        host=register_params.host,
        port=register_params.port
    )
    db.test_connection()
    pass
