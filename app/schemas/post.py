from datetime import datetime
from pydantic import BaseModel

# 생성 
class PostCreate(BaseModel):
    title: str
    body: str

# 수정
class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None

# 응답
class PostResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    class Config:
        from_attributes = True
