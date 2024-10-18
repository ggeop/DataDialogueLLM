
import logging
from fastapi import APIRouter

from app.api.v1.endpoints import (
    root,
    generate,
    agents
)

logger = logging.getLogger(__name__)

api_router = APIRouter()

# Include routers from different endpoint files
api_router.include_router(root.router, tags=["root"])
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
