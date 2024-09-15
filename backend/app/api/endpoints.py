from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import llm_service

router = APIRouter()


class Query(BaseModel):
    text: str


@router.post("/generate")
async def generate_text(query: Query):
    try:
        prompt = f"Human: {query.text}\n\nAssistant:"
        response = llm_service.generate_response(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
