from pydantic import BaseModel, EmailStr
from datetime import datetime

# -------------------------------POSTS---------------------------
                    # -------------------Request----------------------------
class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True

class PostCreate(PostBase):
    pass            # post create is the same as postbase

class PostUpdate(PostBase):
    published: bool # we have to explicitly define published, no more default

            # -------Response------------------
class Post(PostBase):
    # each of these fields can be removed, they dont have to be sent to the user
    id : int 
    # title : str # inherited from PostBase
    # content : str
    # published: bool
    created_at: datetime
    # Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes)

    # recall, when we get back data from database , we get it as an ORM model
    # in order to validate it for sending we need to check whether it's compatible with
    # the pydantic model
    class Config:
        orm_mode = True

#  --------------------------------------------USERS-----------------------------------
    # REQUEST
class UserBase(BaseModel):
    email : EmailStr

class UserCreate(UserBase):
    password: str

    # RESPONSE
class User(UserBase):
    created_at: datetime

    class Config:
        orm_mode = True