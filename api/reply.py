from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/replys",
    tags=['Replys']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Reply)
def create_reply(reply: schemas.ReplyCreate, db: Session = Depends(models.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == reply.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    new_reply = models.Reply(user_id=current_user.id, **reply.dict())
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)

    return new_reply

@router.get("/{id}", response_model=List[schemas.Reply])
def get_replys(id: int, db: Session = Depends(models.get_db), current_user: int = Depends(oauth2.get_current_user)):

    replys = db.query(models.Reply).filter(models.Reply.post_id == id).all()
    
    return replys


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_reply(id: int, db: Session = Depends(models.get_db), current_user: int = Depends(oauth2.get_current_user)):

#     post_query = db.query(models.Post).filter(models.Post.id == id)

#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")

#     if post.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Not authorized to perform requested action")

#     post_query.delete(synchronize_session=False)
#     db.commit()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}", response_model=schemas.Post)
# def update_reply(id: int, updated_post: schemas.PostCreate, db: Session = Depends(models.get_db), current_user: int = Depends(oauth2.get_current_user)):

#     post_query = db.query(models.Post).filter(models.Post.id == id)

#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} does not exist")

#     if post.user_id != current_user.id:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="Not authorized to perform requested action")

#     post_query.update(updated_post.dict(), synchronize_session=False)

#     db.commit()

#     return post_query.first()