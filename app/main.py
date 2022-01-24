from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from . import schemas
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from .utils import *




models.Base.metadata.create_all(bind = engine)




app = FastAPI()
# -------------------------posts-----------------------------

@app.get('/posts', response_model=List[schemas.Post])
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return  posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):   

    # create a new ORM post by unpacking the dictionary
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # retrieve and store it in new_Post
    return  new_post # this is an ORM model

@app.get('/posts/{id}',response_model=schemas.Post)
def get_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first() # get first post with corresponding id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return post


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()

@app.put('/posts/{id}',response_model=schemas.Post)
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



# -------------------------------------users-----------------

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_post(user: schemas.UserCreate, db: Session = Depends(get_db)):   
    # hash password - user.password
    user.password  =  hash_password(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    # retrieve and store it in new_user
    return  new_user # this is an ORM model