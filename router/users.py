from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from model import Users
from authorization.hash import Hash
from authorization.auth import oauth_scheme
from typing import List, Optional

router = APIRouter(tags=["User Detail"])
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for user requests
class UserDetailRequest(BaseModel):
    username: str
    password: str
    phonenumber: int

# Pydantic model for user responses
class UserResponse(BaseModel):
    id: int
    username: str
    phonenumber: Optional[int]

    class Config:
        orm_mode = True

# Get all users with id and username only
@router.get("/userdetails", response_model=List[UserResponse])
def get_all_user_detail(db: Session = Depends(get_db)):
    users = db.query(Users).all()
    return users  # Pydantic will handle the serialization

# Endpoint to register a new user
@router.post("/register")
def create_a_user(user: UserDetailRequest, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt_context(user.password)  # Hash the password
    new_user = Users(username=user.username, password=hashed_password, phonenumber=user.phonenumber)  # Create new user instance
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"Status": "Successfully registered"}

# Endpoint to update the username of an existing user
@router.put("/register/update")
def update_username_of_user(id: int, new_username: str, new_number: int, db: Session = Depends(get_db), token: str = Depends(oauth_scheme)):
    # Query the user by ID
    existing_user = db.query(Users).filter(Users.id == id).first()

    # Check if user exists
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Update the username and commit changes
    existing_user.username = new_username
    existing_user.phonenumber = new_number
    db.commit()
    db.refresh(existing_user)
    
    return {"Status": "Username and phone number updated successfully", "Updated User": {"id": existing_user.id, "username": existing_user.username}}
