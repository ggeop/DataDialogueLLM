import logging

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import RegisterSource
from app.services.data_dialogue import data_dialogue_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/list")
async def get_agents():
    return data_dialogue_service.get_agents()


@router.post("/register")
async def register_source(register_source: RegisterSource):
    try:
        logger.info(f"Starting Register {register_source.sourceType} source")
        data_dialogue_service.register_source(register_source)
        logger.info(f"Register {register_source.sourceType} successful!")
        return JSONResponse(
            content={"message": "Registration successful"},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Failed with error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{agent_name}")
async def delete_agent(agent_name: str):
    try:
        logger.info(f"Attempting to delete agent: {agent_name}")
        data_dialogue_service.delete_agent(agent_name)
        logger.info(f"Successfully deleted agent: {agent_name}")
        return JSONResponse(
            content={"message": f"Agent '{agent_name}' successfully deleted"},
            status_code=status.HTTP_200_OK
        )
    except ValueError as e:
        logger.error(f"Agent not found: {agent_name}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to delete agent {agent_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )