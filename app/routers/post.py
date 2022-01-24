from typing import List
from fastapi import status, HTTPException, Depends,APIRouter
from .. import schemas
from .. import models
from ..database import  get_db
from sqlalchemy.orm import Session
from ..utils import *


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# -------------------------posts-----------------------------

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):   

    # create a new ORM post by unpacking the dictionary
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # retrieve and store it in new_Post
    return  new_post # this is an ORM model

@router.get('/{id}',response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first() # get first post with corresponding id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}',response_model=schemas.Post)
def update_post(id : int, post:schemas.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(old_post)
    return old_post

