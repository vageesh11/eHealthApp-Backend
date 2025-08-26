from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
# from app.connector.postgres_conn import get_db
from datetime import timedelta
from passlib.context import CryptContext
from app.connector.postgres_conn import get_db
from app.schema import models
from app.config.jwt_token import create_access_token,verify_access_token,ACCESS_TOKEN_EXPIRE_MINUTES,ALGORITHM,SECRET_KEY

router = APIRouter()
security = HTTPBearer()
pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#Helper:hash password(for registration)
def get_password_hash(password:str):
    return pwd_context.hash(password)

#get user from DB
def get_user(db:Session,username:str):
    return db.query(models.User).filter(models.User.username==username).first()

# Register route
@router.post("/register")
def register(username:str,password:str,db:Session=Depends(get_db)):
    existing_user=get_user(db,username)
    if existing_user:
        raise HTTPException(status_code=400,detail="Username already registered")
    
    hashed_password=get_password_hash(password)
    new_user=models.User(username=username,password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message":"User registered successfully","username":new_user.username}


#Login route
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user=get_user(db,form_data.username)
    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#Protected route
@router.get("/secure-data")
def secure_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username=verify_access_token(token)
    return {"message": "This is protected data", "user": username}
