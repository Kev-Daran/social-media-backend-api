from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal, Optional

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True


class PostCreate(PostBase):
    pass

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner_id : int
    owner : UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post : PostResponse
    votes : int

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str


class TokenData(BaseModel):
    id : Optional[int] = None

class Votes(BaseModel):
    post_id : int
    dir : Literal[0, 1]
