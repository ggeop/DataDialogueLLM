import logging

from typing import List
from fastapi import APIRouter, HTTPException, status

from app.services.sources.source_manager import source_manager_service
from app.schemas import (
    DataResponse,
    ErrorResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/list",
    response_model=List[str],
    responses={500: {"model": ErrorResponse}},
)
async def get_source_names():
    try:
        supported_sources = source_manager_service.get_source_names()
        if len(supported_sources) == 0:
            return DataResponse(message="Not found supported Sources")
        else:
            return supported_sources
    except Exception as e:
        logger.error(f"Failed to retrieve supported sources: {e}", stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
