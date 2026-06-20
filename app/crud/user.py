from sqlalchemy.orm import Session
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.scrap import Scrap
from app.schemas.user import UserCreate
from app.core.security import hash_password

# 유저 생성
def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        nickname=user.nickname,
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# username으로 유저 찾기 (로그인용)
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# 유저 리스트
def get_users(db: Session):
    return db.query(User).all()

# 유저 상세 조회
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# 프로필 수정
def update_me(db: Session, user_id: int, nickname: str | None, profile_image_url: str | None):
    db_user = db.query(User).filter(User.id == user_id).first()
    if nickname is not None:
        db_user.nickname = nickname
    if profile_image_url is not None:
        db_user.profile_image_url = profile_image_url
    db.commit()
    db.refresh(db_user)
    return db_user

# 유저 검색
def search_users(db: Session, q: str):
    return db.query(User).filter(User.nickname.ilike(f"%{q}%")).all()

# 삭제
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

# 내 게시글
def get_my_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.author_id == user_id).all()

# 내 댓글
def get_my_comments(db: Session, user_id: int):
    return db.query(Comment).filter(Comment.author_id == user_id).all()

# 내가 좋아요한 게시글
def get_my_likes(db: Session, user_id: int):
    likes = db.query(Like).filter(Like.user_id == user_id, Like.post_id != None).all()
    return [like.post for like in likes]

# 내 스크랩
def get_my_scraps(db: Session, user_id: int):
    scraps = db.query(Scrap).filter(Scrap.user_id == user_id).all()
    return [scrap.post for scrap in scraps]