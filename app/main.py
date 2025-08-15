from fastapi import FastAPI
from app.routes import health, testing_routes
from app.connector.postgres_conn import engine, SessionLocal, database_url
from app.schema import models

from app.routes import health,testing_routes

engine,SessionLocal,Base=database_url()

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(health.router)
app.include_router(testing_routes.router)