from fastapi import FastAPI
from app.api.endpoints import router
from app.core.config import settings

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
