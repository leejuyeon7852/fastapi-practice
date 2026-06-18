from datetime import datetime
from pydantic import BaseModel

class LikeResponse(BaseModel):
    liked: bool
    like_count: int
    user_id: int
    user_nickname: str
    post_id: int | None = None
    comment_id: int | None = None
