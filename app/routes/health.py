from fastapi import APIRouter

healthRoute = APIRouter()

@healthRoute.get("/health")
def health_check():
    return {"status": "ok"}