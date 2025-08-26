from fastapi import APIRouter
from app.utils.logger import logger

router = APIRouter()

@router.get("/health")
def health_check():
    logger.debug("Health check endpoint was called")
    return {"status": "ok"}
