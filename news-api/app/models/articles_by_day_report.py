from datetime import date

from pydantic import BaseModel


class ArticlesByDayReport(BaseModel):
    date: date
    article_count: int
