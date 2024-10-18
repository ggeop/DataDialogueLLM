from fastapi.responses import JSONResponse
import logging

from fastapi import (
    APIRouter,
    status,
    HTTPException
)

from app.schemas import Query, DialogueResult
from app.services.data_dialogue import data_dialogue_service
from app.api.v1.endpoints import agents

logger = logging.getLogger(__name__)

api_router = APIRouter()

# Include routers from different endpoint files
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])


@api_router.get("/")
async def root():
    return {"message": "Welcome to Data Dialogue API v1"}


@api_router.get("/healthcheck", status_code=status.HTTP_200_OK)
async def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy"}
    )


@api_router.post("/generate", response_model=DialogueResult)
async def generate_text(query: Query):
    try:
        agent = data_dialogue_service.get_agent(query.agent)
        logger.info(f"Selected Agent: {agent.name}")
        response = agent.generate(query.text)
        return response
    except Exception as e:
        logger.error(f"Failed with error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e))
