
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import agents, api
from app.core.config import settings

app = FastAPI()

app.include_router(
    agents.router,
    prefix="/agents",
    tags=["agents"]
)
app.include_router(
    api.router,
    prefix="/api",
    tags=["generate"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
