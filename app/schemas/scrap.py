from pydantic import BaseModel

class ScrapResponse(BaseModel):
    scraped: bool
    scrap_count: int
    post_id: int | None = None
