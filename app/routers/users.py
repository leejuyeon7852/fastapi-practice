from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.crud import user as user_crud
from app.schemas.user import UserCreate, UserLogin, UserResponse, UserProfileResponse, Token
from app.schemas.post import PostResponse
from app.schemas.comment import CommentResponse
from app.core.security import verify_password, create_access_token
from app.core.deps import get_db, get_current_user
from app.models.user import User
import shutil, uuid, os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/users")

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

# 내 정보 조회 (마이페이지)
@router.get("/me", response_model=UserProfileResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# 유저 검색
@router.get("/search", response_model=list[UserResponse])
async def search_users(q: str, db: Session = Depends(get_db)):
    return user_crud.search_users(db, q)

# 내 게시글 목록
@router.get("/me/posts", response_model=list[PostResponse])
async def get_my_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.get_my_posts(db, current_user.id)

# 내 댓글 목록
@router.get("/me/comments", response_model=list[CommentResponse])
async def get_my_comments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.get_my_comments(db, current_user.id)

# 내가 좋아요한 게시글 목록
@router.get("/me/likes", response_model=list[PostResponse])
async def get_my_likes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.get_my_likes(db, current_user.id)

# 내 스크랩 목록
@router.get("/me/scraps", response_model=list[PostResponse])
async def get_my_scraps(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_crud.get_my_scraps(db, current_user.id)

# 타인 프로필 조회
@router.get("/{user_id}", response_model=UserProfileResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="유저를 찾을 수 없습니다.")
    return db_user

# 타인 게시글 목록
@router.get("/{user_id}/posts", response_model=list[PostResponse])
async def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    return user_crud.get_my_posts(db, user_id)

# 프로필 수정
@router.put("/me", response_model=UserProfileResponse)
async def update_me(
    nickname: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = None
    if image:
        ext = image.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(UPLOAD_DIR, filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        image_url = f"/{UPLOAD_DIR}/{filename}"
    return user_crud.update_me(db, current_user.id, nickname=nickname, profile_image_url=image_url)
