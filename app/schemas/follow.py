from pydantic import BaseModel

class FollowResponse(BaseModel):
    followed: bool
    following_id: int

class FollowUserResponse(BaseModel):
    id: int
    username: str
    nickname: str

    class Config:
        from_attributes = True
