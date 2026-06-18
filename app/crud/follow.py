from sqlalchemy.orm import Session
from app.models.follow import Follow
from app.schemas.follow import FollowResponse

def toggle_follow(db: Session, follower_id: int, following_id: int) -> FollowResponse:
    existing = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.following_id == following_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        followed = False
    else:
        new_follow = Follow(follower_id=follower_id, following_id=following_id)
        db.add(new_follow)
        db.commit()
        followed = True

    return FollowResponse(followed=followed, following_id=following_id)

def get_followers(db: Session, user_id: int):
    follows = db.query(Follow).filter(Follow.following_id == user_id).all()
    return [f.follower for f in follows]

def get_following(db: Session, user_id: int):
    follows = db.query(Follow).filter(Follow.follower_id == user_id).all()
    return [f.following for f in follows]
