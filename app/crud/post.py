from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

# 게시글 생성
def create_post(db: Session, post: PostCreate):
    db_post = Post(
        title=post.title,
        body=post.body
    )

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    return db_post

# 게시글 전체 조회
def get_posts(db: Session):
    return db.query(Post).all()

# 게시글 상세 조회
def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

# 게시글 수정
def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if db_post is None:
        return None
    
    if post.title is not None:
        db_post.title = post.title
    
    if post.body is not None:
        db_post.body = post.body
    
    db.commit()
    db.refresh(db_post)

    return db_post

# 게시글 삭제
def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()

    if db_post is None:
        return None
    
    db.delete(db_post)
    db.commit()

    return db_post
