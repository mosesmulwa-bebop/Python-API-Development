
from fastapi import  status, HTTPException, Depends, APIRouter
from .. import schemas
from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import *

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# -------------------------------------users-----------------

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):   
    # hash password - user.password
    user.password  =  hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    # retrieve and store it in new_user
    return  new_user # this is an ORM model

@router.get('/{id}',response_model=schemas.User)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() # get first user with corresponding id
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} not found")
    return user
