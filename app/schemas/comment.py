from datetime import datetime
from pydantic import BaseModel, model_validator

# 생성
class CommentCreate(BaseModel):
    body: str

# 응답
class CommentResponse(BaseModel):
    id: int
    post_id: int
    author_id: int
    author_nickname: str
    parent_id: int | None = None
    body: str
    created_at: datetime
    replies: list["CommentResponse"] = []

    @model_validator(mode="before")
    @classmethod
    def fill_author_nickname(cls, obj):
        if hasattr(obj, "author") and obj.author:
            obj.__dict__["author_nickname"] = obj.author.nickname
        return obj

    class Config:
        from_attributes = True

CommentResponse.model_rebuild()