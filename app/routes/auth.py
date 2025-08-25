from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta

from app.config.jwt_token import create_access_token,verify_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY

router = APIRouter()
security = HTTPBearer()


#Login route
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Protected route
@router.get("/secure-data")
def secure_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username=verify_access_token(token)
    return {"message": "This is protected data", "user": username}
