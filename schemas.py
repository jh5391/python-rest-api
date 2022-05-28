from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    
class PostCreate(PostBase):
    pass
    
class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
#    votes: int

    class Config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None