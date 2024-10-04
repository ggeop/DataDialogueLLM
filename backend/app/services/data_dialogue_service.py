import logging

from app.models.database import Database, SQLiteDatabase
from app.models.language_model import SQLLlamaModel, GeneralLlamaModel
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


def update_data_dialogue_service(database: Database):
    global data_dialogue_service
    pass
