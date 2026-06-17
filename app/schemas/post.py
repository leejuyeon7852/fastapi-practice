from datetime import datetime
from pydantic import BaseModel, model_validator

# 생성
class PostCreate(BaseModel):
    title: str
    body: str
    image_url: str | None = None

# 수정
class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    image_url: str | None = None

# 응답
class PostResponse(BaseModel):
    id: int
    author_id: int
    author_nickname: str
    title: str
    body: str
    image_url: str | None = None
    created_at: datetime

    @model_validator(mode="before")
    @classmethod
    def fill_author_nickname(cls, obj):
        if hasattr(obj, "author") and obj.author:
            obj.__dict__["author_nickname"] = obj.author.nickname
        return obj

    class Config:
        from_attributes = True
