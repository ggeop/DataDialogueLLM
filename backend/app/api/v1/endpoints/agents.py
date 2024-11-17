import logging
from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.schemas import RegisterAgent
from app.services.agents.agent_manager import agent_manager_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/list")
async def get_agents():
    return agent_manager_service.get_agents()


@router.post("/register")
async def register(register_agent: RegisterAgent):
    try:
        logger.info(
            f"Starting Register {register_agent.sourceType} source and model type {register_agent.agentType}"
        )
        agent_manager_service.register_agent(register_agent)
        logger.info(f"Register {register_agent.sourceType} successful!")
        return JSONResponse(
            content={"message": "Registration successful"},
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"Failed with error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/{agent_name}")
async def delete_agent(agent_name: str):
    try:
        agent_name = unquote(agent_name)
        logger.info(f"Attempting to delete agent: {agent_name}")
        agent_manager_service.delete_agent(agent_name)
        logger.info(f"Successfully deleted agent: {agent_name}")
        return JSONResponse(
            content={"message": f"Agent '{agent_name}' successfully deleted"},
            status_code=status.HTTP_200_OK,
        )
    except ValueError as e:
        logger.error(f"Agent not found: {agent_name}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to delete agent {agent_name}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
