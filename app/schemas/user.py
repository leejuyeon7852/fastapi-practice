from datetime import datetime
from pydantic import BaseModel, model_validator

# 회원가입
class UserCreate(BaseModel):
    username: str
    nickname: str
    email: str
    password: str

# 로그인
class UserLogin(BaseModel):
    username: str
    password: str

# 토큰 응답
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# 유저 응답
class UserResponse(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

# 마이페이지 응답
class UserProfileResponse(BaseModel):
    id: int
    nickname: str
    profile_image_url: str | None = None
    follower_count: int = 0
    following_count: int = 0

    @model_validator(mode="before")
    @classmethod
    def fill_counts(cls, obj):
        if hasattr(obj, "followers"):
            obj.__dict__["follower_count"] = len(obj.followers)
        if hasattr(obj, "following"):
            obj.__dict__["following_count"] = len(obj.following)
        return obj

    class Config:
        from_attributes = True
