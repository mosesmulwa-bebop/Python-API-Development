from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2 
from psycopg2.extras import RealDictCursor
from app.mycred import credentials
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind = engine)

app = FastAPI()





class Post(BaseModel):
    title : str
    content : str
    published: bool = True

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "success"}