import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.schemas import (
    Query,
    RegisterSource
)
from app.services.data_dialogue import (
    get_data_dialogue_agent,
    register_data_source
)


router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.post("/generate")
async def generate_text(query: Query):
    try:
        agent = get_data_dialogue_agent(query.model)
        logger.info(f"Selected model {agent.model.alias}")
        response = agent.generate(query.text)
        return response
    except Exception as e:
        logger.error(f"Failed with error {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register")
async def register_source(register_source: RegisterSource):
    try:
        logger.info(f"Starting Register {register_source.sourceType} source")
        register_data_source(register_source)
        logger.info(f"Register {register_source.sourceType} successful!")
        return JSONResponse(content={"message": "Registration successful"}, status_code=200)
    except Exception as e:
        logger.error(f"Failed with error {e}")
        raise HTTPException(status_code=500, detail=str(e))
