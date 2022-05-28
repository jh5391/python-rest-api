from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(models.get_db), current_user: int = Depends(oauth2.get_current_user)):

    posts = db.query(models.Post).all()
    # db.query(models.Post).join(
    #     models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(models.get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post