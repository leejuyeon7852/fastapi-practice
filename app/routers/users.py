from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 회원가입
@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing = user_crud.get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="이미 사용 중인 아이디입니다.")
    return user_crud.create_user(db, user)

# 로그인
@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 틀렸습니다.")
    token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

# 내 정보 조회
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
