from datetime import datetime
from pydantic import BaseModel

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
