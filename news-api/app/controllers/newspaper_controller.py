from datetime import date, timedelta

from fastapi import APIRouter, Body, HTTPException
from peewee import fn

from app.controllers.base_controller import BaseController
from app.entities.news_article_entity import NewsArticleEntity
from app.entities.newspaper_entity import NewspaperEntity
from app.models.articles_by_day_report import ArticlesByDayReport
from app.models.newspaper import Newspaper
from app.services.base_service import BaseService


class NewspaperController(BaseController):
    def __init__(self):
        BaseController.__init__(
            self, Newspaper, NewspaperEntity, BaseService(NewspaperEntity)
        )


controller = NewspaperController()


def get_newspaper_controller() -> NewspaperController:
    return controller
