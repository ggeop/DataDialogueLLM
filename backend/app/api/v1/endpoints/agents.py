import logging
from urllib.parse import unquote

from fastapi import APIRouter, HTTPException, status

from app.services.agents.agent_manager import agent_manager_service
from app.schemas import (
    BaseResponse,
    DataResponse,
    ErrorResponse,
    RegisterAgent,
    AgentList,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/list",
    response_model=DataResponse[AgentList],
    responses={500: {"model": ErrorResponse}},
)
async def get_agent_names():
    try:
        agents = agent_manager_service.get_agent_names()
        if len(agents) == 0:
            return DataResponse(
                message="Not found register Agents", data=AgentList(agents=agents)
            )
        else:
            return DataResponse(
                message=f"{len(agents)} Agents retrieved successfully",
                data=AgentList(agents=agents),
            )
    except Exception as e:
        logger.error(f"Failed to retrieve agents: {e}", stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post(
    "/register", response_model=BaseResponse, responses={500: {"model": ErrorResponse}}
)
async def register(register_agent: RegisterAgent):
    try:
        logger.info(
            f"Starting Register {register_agent.sourceType} source and model type {register_agent.agentType}"
        )
        agent_manager_service.register_agent(register_agent)
        logger.info(f"Register {register_agent.sourceType} successful!")
        return BaseResponse(message="Registration successful")
    except Exception as e:
        logger.error(f"Failed with error {e}", stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete(
    "/{agent_name}",
    response_model=BaseResponse,
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
)
async def delete_agent(agent_name: str):
    """Delete an agent by name"""
    try:
        agent_name = unquote(agent_name)
        logger.info(f"Attempting to delete agent: {agent_name}")
        agent_manager_service.delete_agent(agent_name)
        logger.info(f"Successfully deleted agent: {agent_name}")
        return BaseResponse(message=f"Agent '{agent_name}' successfully deleted")
    except ValueError as e:
        logger.error(f"Agent not found: {agent_name}", stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_name}' not found with error: {e}",
        )
    except Exception as e:
        logger.error(f"Failed to delete agent {agent_name}: {e}", stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
