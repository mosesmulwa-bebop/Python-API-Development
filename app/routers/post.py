from typing import List, Optional
from fastapi import status, HTTPException, Depends,APIRouter
from .. import schemas
from .. import models
from ..database import  get_db
from sqlalchemy.orm import Session
from ..utils import *
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# -------------------------posts-----------------------------

@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
 current_user  = Depends(oauth2.get_current_user),
 limit:int = 10,skip:int = 0,search:Optional[str]= ""):
    #get posts from current user only
    #posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()
    #get posts from all users
   
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
 current_user = Depends(oauth2.get_current_user)):   
    # create a new ORM post by unpacking the dictionary
    post_dict = post.dict()
    post_dict['user_id'] =current_user.id
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # retrieve and store it in new_Post
    return  new_post # this is an ORM model

@router.get('/{id}',response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db),
 current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first() # get first post with corresponding id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db),
 current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

@router.put('/{id}',response_model=schemas.Post)
def update_post(id : int, post:schemas.PostUpdate, db: Session = Depends(get_db),
 current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    if old_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform requested action")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(old_post)
    return old_post


