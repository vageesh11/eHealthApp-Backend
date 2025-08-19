from fastapi import APIRouter
from app.utils.logger import logger

healthRoute = APIRouter()

@healthRoute.get("/health")
def health_check():
    logger.debug("Health check endpoint was called")
    return {"status": "ok"}