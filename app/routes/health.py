from fastapi import APIRouter
from app.logging.logger import logger

healthRoute = APIRouter()

@healthRoute.get("/health")
def health_check():
    logger.info("Health check endpoint was called")
    return {"status": "ok"}