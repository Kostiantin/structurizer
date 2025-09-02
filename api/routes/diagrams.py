# My updated diagrams route
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.generate_diagram import generate_diagram
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class DiagramRequest(BaseModel):
    text: str
    diagram_type: str = "flowchart"

@router.post("/")
async def diagrams(request: DiagramRequest):
    try:
        logger.info(f"Received diagram request: {request.text[:50]}...")
        diagram = generate_diagram(request.text, request.diagram_type)
        logger.info("Diagram generation successful")
        return {"diagram": diagram}
    except Exception as e:
        logger.error(f"Diagram generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Diagram generation error: {str(e)}")

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