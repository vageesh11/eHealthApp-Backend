from fastapi import FastAPI
from app.utils.logger import logger   # fixed path: logging/logger.py
from app.routes import health, auth
from app.routes import auth
from app.connector.postgres_conn import engine,Base
import app.schema.models


app = FastAPI()

# Include Routers
app.include_router(auth.router)
# app.include_router(health.healthRoute, prefix="/health", tags=["Health"])
# app.include_router(auth.router, prefix="/auth", tags=["Auth"])
# app.include_router(testing_routes.router, prefix="/test", tags=["Testing"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    # logger.info("Root endpoint was called")
    return {"message": "Hello, World!"}
