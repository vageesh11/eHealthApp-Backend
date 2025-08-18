from fastapi import FastAPI
from app.utils.logger import logger
from app.routes import health

app = FastAPI()

app.include_router(health.healthRoute)

@app.get("/")
def root():
    logger.info("Root endpoint was called")
    return {"message":"Hello,World!"}