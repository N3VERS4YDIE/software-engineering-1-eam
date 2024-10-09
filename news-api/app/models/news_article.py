from datetime import date

from pydantic import BaseModel


class NewsArticle(BaseModel):
    id: int
    newspaper_id: int
    title: str
    content: str
    date_uploaded: date
