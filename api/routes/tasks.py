# My updated tasks route
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.extract_tasks import extract_tasks
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class TasksRequest(BaseModel):
    text: str

@router.post("/")
async def tasks(request: TasksRequest):
    try:
        logger.info(f"Received tasks request: {request.text[:50]}...")
        tasks = extract_tasks(request.text)
        logger.info("Tasks extraction successful")
        return {"tasks": tasks}
    except Exception as e:
        logger.error(f"Tasks extraction failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Tasks extraction error: {str(e)}")

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