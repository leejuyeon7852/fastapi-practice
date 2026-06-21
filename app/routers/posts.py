from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil, uuid, os

from app.crud import post as post_crud
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.core.deps import get_db, get_current_user
from app.models.user import User
from app.models.post import Post
from app.models.like import Like
from app.models.scrap import Scrap
from app.models.follow import Follow

router = APIRouter(prefix="/posts")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(image: UploadFile) -> str:
    ext = image.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    return f"/{UPLOAD_DIR}/{filename}"

# 게시글 생성
@router.post("/", response_model=PostResponse)
async def create_post(
    title: str = Form(...),
    body: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = save_image(image) if image else None
    post_data = PostCreate(title=title, body=body, image_url=image_url)
    return post_crud.create_post(db, post_data, current_user.id)

# 게시글 전체 조회
@router.get("/", response_model=list[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    return post_crud.get_posts(db)

# 팔로잉 피드
@router.get("/feed", response_model=list[PostResponse])
async def get_feed(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    following = db.query(Follow).filter(Follow.follower_id == current_user.id).all()
    following_ids = [f.following_id for f in following]
    if not following_ids:
        return []
    return db.query(Post).filter(Post.author_id.in_(following_ids)).order_by(Post.id.desc()).all()

# 게시글 검색
@router.get("/search", response_model=list[PostResponse])
async def search_posts(q: str, db: Session = Depends(get_db)):
    return post_crud.search_posts(db, q)

# 게시글 상세 조회
@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# 게시글 수정
@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    title: str | None = Form(None),
    body: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = save_image(image) if image else None
    post_data = PostUpdate(title=title, body=body, image_url=image_url)
    db_post = post_crud.update_post(db, post_id, post_data, current_user.id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post == "forbidden":
        raise HTTPException(status_code=403, detail="본인 게시글만 수정할 수 있습니다.")
    return db_post

# 좋아요 상태 조회
@router.get("/{post_id}/like/status")
async def get_like_status(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    liked = db.query(Like).filter(Like.user_id == current_user.id, Like.post_id == post_id).first() is not None
    count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"liked": liked, "like_count": count}

# 스크랩 상태 조회
@router.get("/{post_id}/scrap/status")
async def get_scrap_status(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    scraped = db.query(Scrap).filter(Scrap.user_id == current_user.id, Scrap.post_id == post_id).first() is not None
    count = db.query(Scrap).filter(Scrap.post_id == post_id).count()
    return {"scraped": scraped, "scrap_count": count}

# 게시글 삭제
@router.delete("/{post_id}")
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = post_crud.delete_post(db, post_id, current_user.id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post == "forbidden":
        raise HTTPException(status_code=403, detail="본인 게시글만 삭제할 수 있습니다.")
    return {"message": "게시글이 삭제되었습니다."}
