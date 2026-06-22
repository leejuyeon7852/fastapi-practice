from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    follower = relationship("User", foreign_keys=[follower_id], overlaps="following")
    following = relationship("User", foreign_keys=[following_id], overlaps="followers")

    __table_args__ = (
        UniqueConstraint("follower_id", "following_id", name="uq_follow"),
    )
