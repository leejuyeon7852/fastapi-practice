from sqlalchemy.orm import Session
from app.models.like import Like
from app.schemas.like import LikeResponse

def toggle_like(
        db: Session, user_id: int, user_nickname:str, 
        post_id: int | None = None, comment_id: int | None = None
    ) -> LikeResponse :
    query = db.query(Like).filter(Like.user_id == user_id)

    if post_id:
        query = query.filter(Like.post_id == post_id)
    if comment_id:
        query = query.filter(Like.comment_id == comment_id)
    
    existing = query.first()

    if existing:
        db.delete(existing)
        db.commit()
        liked = False
    else:
        new_like = Like(user_id=user_id, post_id=post_id, comment_id=comment_id)
        db.add(new_like)
        db.commit()
        liked= True
    
    if post_id:
        count = db.query(Like).filter(Like.post_id == post_id).count()
    else:
        count = db.query(Like).filter(Like.comment_id == comment_id).count()

    return LikeResponse(
        liked=liked,
        like_count=count,
        user_id=user_id,
        user_nickname=user_nickname,
        post_id=post_id,
        comment_id=comment_id
    )