import logging

from fastapi import (
    APIRouter,
    HTTPException,
    status
)

from app.schemas import Query, DialogueResult
from app.services.data_dialogue import data_dialogue_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=DialogueResult)
async def generate_text(query: Query):
    try:
        agent = data_dialogue_service.get_agent(query.model)
        logger.info(f"Selected model {agent.model.alias}")
        response = agent.generate(query.text)
        return response
    except Exception as e:
        logger.error(f"Failed with error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
