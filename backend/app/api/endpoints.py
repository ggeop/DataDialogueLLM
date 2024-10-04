import logging
from fastapi import APIRouter, HTTPException, Depends

from app.schemas.request_response import (
    Query,
    RegisterSource
)
from app.services.data_dialogue_service import (
    get_data_dialogue_service,
    update_data_dialogue_service
)


router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.post("/generate")
async def generate_text(query: Query, service=Depends(get_data_dialogue_service)):
    try:
        response = service.generate(query.text)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register")
async def register_source(register_source: RegisterSource):
    try:
        #update_data_dialogue_service()
        logger.info(f"Register successful!! data:{register_source}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
