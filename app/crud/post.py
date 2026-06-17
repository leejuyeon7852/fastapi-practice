from sqlalchemy.orm import Session
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate

# 게시글 생성
def create_post(db: Session, post: PostCreate, author_id: int):
    db_post = Post(
        title=post.title,
        body=post.body,
        author_id=author_id,
        image_url=post.image_url
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
def update_post(db: Session, post_id: int, post: PostUpdate, author_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        return None
    if db_post.author_id != author_id:
        return "forbidden"
    if post.title is not None:
        db_post.title = post.title
    if post.body is not None:
        db_post.body = post.body
    if post.image_url is not None:
        db_post.image_url = post.image_url
    db.commit()
    db.refresh(db_post)
    return db_post

# 게시글 삭제
def delete_post(db: Session, post_id: int, author_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        return None
    if db_post.author_id != author_id:
        return "forbidden"
    db.delete(db_post)
    db.commit()
    return db_post
