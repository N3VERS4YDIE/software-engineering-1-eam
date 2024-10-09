from fastapi import APIRouter

from app.controllers.base_controller import BaseController
from app.controllers.faker_controller import get_faker_router
from app.controllers.newspaper_controller import get_newspaper_controller
from app.controllers.report_controller import get_report_router
from app.controllers.test_controller import get_test_router
from app.entities.news_article_entity import NewsArticleEntity
from app.entities.newspaper_entity import NewspaperEntity
from app.models.news_article import NewsArticle
from app.models.newspaper import Newspaper
from app.services.base_service import BaseService

router = APIRouter()

newspaper_service = BaseService(NewspaperEntity)
news_article_service = BaseService(NewsArticleEntity)

newspaper_controller = get_newspaper_controller()
news_article_controller = BaseController(
    NewsArticle, NewsArticleEntity, news_article_service
)

router.include_router(
    newspaper_controller.get_router(),
    prefix="/newspapers",
    tags=["Newspapers"],
)

router.include_router(
    news_article_controller.get_router(),
    prefix="/news-articles",
    tags=["News Articles"],
)

router.include_router(get_report_router(), prefix="/reports", tags=["Reports"])
router.include_router(get_test_router(), prefix="/tests", tags=["Tests"])
router.include_router(get_faker_router(), prefix="/faker", tags=["Faker"])
