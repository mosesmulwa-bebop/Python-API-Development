from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating : Optional[int] = None

my_posts = [{"title" : "title of post 1", "content":"content1", "id": 1},
{"title" : "title of post 2", "content":"content2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p



@app.get("/")
def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):   # fast api automatically validates if this is a valid post
    # new post variable now has title and content
    # print(post.rating)
    # convert pydantic model to dictionary
    # print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get('/posts/{id}')
def get_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    return {"post_detail": post}   


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    else:
        # get the index of post
        index = my_posts.index(post)
        my_posts.pop(index)
        return {"post_detail": post}   

@app.put('/posts/{id}')
def update_post(id : int, post:Post):
    old_post = find_post(id)
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    else:
        index = my_posts.index(old_post)
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {"post_detail": post_dict}  