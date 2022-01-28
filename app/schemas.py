from ast import Pass
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime



#  --------------------------------------------USERS-----------------------------------
    # REQUEST
class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserCreate):
    Pass



    # RESPONSE
class User(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True

# ------------------------------------Votes----------------------------------
#---           ----- ---------REQUEST
class VoteCreate(BaseModel):
    post_id:int
    dir: bool

class Vote(BaseModel):
    post_id: int
    user_id: int

    class Config:
        orm_mode = True





# -----------------------------------TOKEN---------------
class Token(BaseModel):
    access_token : str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



# -------------------------------POSTS---------------------------
                    # -------------------Request----------------------------
class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True

class PostCreate(PostBase):
    Pass
               

class PostUpdate(PostBase):
    published: bool # we have to explicitly define published, no more default

            # -------Response------------------
class Post(PostCreate):
    # each of these fields can be removed, they dont have to be sent to the user
    id : int 
    # title : str # inherited from PosCreate
    # content : str
    # published: bool
    created_at: datetime
    user_id: int
    owner: User
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes)

    # recall, when we get back data from database , we get it as an ORM model
    # in order to validate it for sending we need to check whether it's compatible with
    # the pydantic model
    class Config:
        orm_mode = True




class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
