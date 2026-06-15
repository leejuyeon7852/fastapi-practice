from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)
    created_at = Column(DateTime, default=datetime.now)
