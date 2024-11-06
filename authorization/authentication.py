from fastapi import APIRouter,HTTPException,Depends
from authentication import auth
import model
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from authentication.hash import Hash

router = APIRouter(
    tags=['authentication']
)

def get_db():
    db=SessionLocal()
    try:
        yield(db)
    finally:
        db.close()
        
@router.post('/token')
def get_token(request:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    employee=db.query(model.Employee).filter(model.Employee.username==request.username).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid credentials")
    if not Hash.verify(request.password,Hash.bcrypt_context(employee.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid password")
    access_token=auth.create_access_token(data={'sub':employee.username,'id':employee.id})
    
    return{
        'access_token':access_token,
        'token_type':'bearer',
        'username':employee.username,
        'id':employee.id
    }