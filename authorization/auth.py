from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from typing import Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from model import Users  # Make sure you have a Users model to query against
from authorization.hash import Hash  # Assuming you have a Hash utility to verify passwords
from database import SessionLocal

SECRET_KEY = "db9e8812f86488fe8d20057c03961b0c124660176957bfd9fd2f46ed70fa04ae"
ALGORITHM = 'HS256'
TOKEN_EXPIRE_TIME = 20

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')
router = APIRouter()  # Create an instance of APIRouter

def create_access_token(data: dict, expire_time: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expire_time if expire_time else timedelta(minutes=TOKEN_EXPIRE_TIME))
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

@router.post("/token")  # Endpoint to handle login
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == username).first()
    if not user or not Hash.verify_password(password, user.password):  # Use Hash utility to check password
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})  # Create a token with user data
    return {"access_token": access_token, "token_type": "bearer"}

# You can add more routes related to authorization here
