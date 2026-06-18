from sqlalchemy.orm import Session
from app.models.scrap import Scrap
from app.schemas.scrap import ScrapResponse

def toggle_scrap(db: Session, user_id: int, post_id: int) -> ScrapResponse :
    existing = db.query(Scrap).filter(
        Scrap.user_id == user_id,
        Scrap.post_id == post_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()
        scraped = False
    else:
        new_scrap = Scrap(user_id=user_id, post_id=post_id)
        db.add(new_scrap)
        db.commit()
        scraped = True
    
    count = db.query(Scrap).filter(Scrap.post_id == post_id).count()

    return ScrapResponse(scraped=scraped, scrap_count=count, post_id=post_id)
