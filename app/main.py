from turtle import pos
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind = engine)

app = FastAPI()


class Post(BaseModel):
    title : str
    content : str
    published: bool = True

@app.get('/posts')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data" : posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):   

    # create a new post by unpacking the dictionary
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # retrieve and store it in new_Post
    return {"data": new_post}

@app.get('/posts/{id}')
def get_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first() # get first post with corresponding id
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return {"data" : post}  


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return {"Post deleted": post}   

@app.put('/posts/{id}')
def update_post(id : int, post:Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_post = post_query.first()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(old_post)
    return {"Post updated": old_post}  