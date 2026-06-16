from sqlalchemy.orm import Session
from app.models.user import User
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

# 삭제
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
