from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    nickname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile_image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    followers = relationship("Follow", foreign_keys="Follow.following_id", back_populates=None)
    following = relationship("Follow", foreign_keys="Follow.follower_id", back_populates=None)

