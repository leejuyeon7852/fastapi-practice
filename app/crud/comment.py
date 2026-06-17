from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

# 댓글 생성
def create_comment(db: Session, post_id: int, author_id: int, comment: CommentCreate, parent_id: int | None = None):
    db_comment = Comment(
        post_id=post_id,
        author_id=author_id,
        parent_id=parent_id,
        body=comment.body
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# 댓글 전체 조회 (대댓글 제외 — 최상위 댓글만)
def get_comments(db: Session, post_id: int):
    return db.query(Comment).filter(
        Comment.post_id == post_id,
        Comment.parent_id == None
    ).all()

# 댓글 삭제
def delete_comment(db: Session, comment_id: int, author_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        return None
    if db_comment.author_id != author_id:
        return "forbidden"
    db.delete(db_comment)
    db.commit()
    return db_comment