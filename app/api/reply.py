from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, oauth2

router = APIRouter(prefix="/replys", tags=["Replys"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Reply)
def create_reply(
    reply: schemas.ReplyCreate,
    db: Session = Depends(models.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == reply.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    new_reply = models.Reply(user_id=current_user.id, **reply.dict())
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)

    return new_reply


@router.get("/{id}", response_model=List[schemas.Reply])
def get_replys(
    id: int,
    db: Session = Depends(models.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    replys = db.query(models.Reply).filter(models.Reply.post_id == id).all()

    return replys


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reply(
    id: int,
    db: Session = Depends(models.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    reply_query = db.query(models.Reply).filter(models.Reply.id == id)

    reply = reply_query.first()

    reply_join = (
        db.query(models.Post, models.Reply)
        .join(models.Reply, models.Reply.post_id == models.Post.id)
        .filter(models.Reply.id == id)
        .first()
    )
    owner_id = reply_join[0].user_id

    if reply == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"reply with id: {id} does not exist",
        )

    if reply.user_id != current_user.id or owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    reply_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Reply)
def update_reply(
    id: int,
    updated_reply: schemas.ReplyCreate,
    db: Session = Depends(models.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):

    reply_query = db.query(models.Reply).filter(models.Reply.id == id)

    reply = reply_query.first()

    reply_join = (
        db.query(models.Post, models.Reply)
        .join(models.Reply, models.Reply.post_id == models.Post.id)
        .filter(models.Reply.id == id)
        .first()
    )
    owner_id = reply_join[0].user_id

    if reply == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"reply with id: {id} does not exist",
        )

    if reply.user_id != current_user.id or owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    reply_query.update(updated_reply.dict(), synchronize_session=False)

    db.commit()

    return reply_query.first()
