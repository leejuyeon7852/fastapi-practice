from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import scrap as scrap_crud
from app.schemas.scraps import ScrapResponse
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

# 스크랩 토글
@router.post("/posts/{post_id}/scrap", response_model=ScrapResponse)
async def toggle_scrap(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return scrap_crud.toggle_scrap(db, current_user.id, post_id)
