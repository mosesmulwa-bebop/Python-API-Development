from fastapi import FastAPI
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    '*' #wildcard
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8080",
    # "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)




@app.get('/')
def home():
    return {'message':"hello world"}




#Using SQLalchemy to generate db
# #from . import models
#from .database import engine
#from .config import settings
#models.Base.metadata.create_all(bind = engine)
