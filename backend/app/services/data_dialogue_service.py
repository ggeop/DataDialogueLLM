import logging

from app.models.database import Database, PostgresDatabase
from app.models.language_model import SQLLlamaModel, GeneralLlamaModel
from app.schemas.request_response import RegisterSource
from app.agents.data_dialogue_agent import DataDialogueAgent
from app.services.database_service import create_examples_database
from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# Service Initialization
database = create_examples_database()
data_dialogue_service = DataDialogueAgent(
    database=database,
    sql_model=SQLLlamaModel(settings.MODEL_PATH),
    general_model=GeneralLlamaModel(settings.MODEL_PATH)
)


def get_data_dialogue_service():
    global data_dialogue_service
    return data_dialogue_service


def update_data_dialogue_service(register_params: RegisterSource):
    global data_dialogue_service
    logger.info(f"Try to register with params: {register_params}")
    db = PostgresDatabase(
        dbname=register_params.dbname,
        user=register_params.username,
        password=register_params.password,
        host=register_params.host,
        port=register_params.port
    )
    db.test_connection()
    pass
