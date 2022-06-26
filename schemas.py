from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


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

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class ReplyBase(BaseModel):
    post_id: int
    comment: str


class ReplyCreate(ReplyBase):
    pass


class Reply(ReplyBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class ReplyOut(BaseModel):
    Reply: Reply

    class Config:
        orm_mode = True
