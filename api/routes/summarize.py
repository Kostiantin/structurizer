# My updated summarization route
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.summarize_workshop import summarize_workshop
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str

@router.post("/")
async def summarize(request: SummarizeRequest):
    try:
        logger.info(f"Received summarization request: {request.text[:50]}...")
        summary = summarize_workshop(request.text)
        logger.info("Summarization successful")
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Summarization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")

@router.options("/")
async def options():
    return {
        "status_code": 200,
        "headers": {
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    }