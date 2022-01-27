from fastapi import  status, HTTPException, Depends, APIRouter
from .. import schemas,models,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import *


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteCreate, db: Session = Depends(get_db), 
                current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post Not found")

    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, 
                                                    models.Vote.post_id == vote.post_id) 
    if vote.dir == True:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")

        new_vote_dict ={"post_id":vote.post_id, "user_id": current_user.id}
        new_vote = models.Vote(**new_vote_dict)
        db.add(new_vote)
        db.commit()
        
        return {"message":"successfully added vote"}

    elif vote.dir == False:
        if not vote_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote Not found")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted vote"}