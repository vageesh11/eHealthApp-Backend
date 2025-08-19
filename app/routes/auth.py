from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime,timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter()

SECRET_KEY = "poiuytrewq234567890asdfghjkl" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#OAuth2 schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

#Dummy user (later fetch from DB)
fake_user = {
    "username": "rahamath",
    "hashed_password": "$2b$12$qPxErL3IQD0v4fht6F5QWeBzTSl/mvB3l8q0nZhB4WMoRxu5Gm7D2"
}

#create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#Authenticate user
def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False
    if password != "2323":  
        return False
    return True

#Login route
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# HTTPBearer security dependency
security = HTTPBearer()

#Protected route
@router.get("/secure-data")
def secure_data(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"message": "This is protected data", "user": username}
