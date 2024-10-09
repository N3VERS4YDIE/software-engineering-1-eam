from fastapi import APIRouter, Query
from faker import Faker
from peewee import IntegrityError
from datetime import date, timedelta
from app.entities.news_article_entity import NewsArticleEntity
from app.entities.newspaper_entity import NewspaperEntity
from app.db import get_db

fake = Faker()
faker_router = APIRouter()


def get_faker_router():
    return faker_router


@faker_router.get("/create-newspapers-articles")
async def create_newspapers_articles(
    newspapers_count: int = Query(..., description="Number of newspapers to create"),
    articles_count: int = Query(..., description="Number of articles per newspaper"),
):
    for _ in range(newspapers_count):
        newspaper = create_newspaper()
        if newspaper:
            for _ in range(articles_count):
                create_news_article(newspaper)

    return {
        "msg": f"Succesfully created {newspapers_count} newspapers with {articles_count} articles"
    }


def create_newspaper():
    """Creates a fake newspaper entity."""
    try:
        newspaper = NewspaperEntity.create(
            name=fake.company(),
            email=fake.email(),
        )
        print(f"Created Newspaper: {newspaper.name} - {newspaper.email}")
        return newspaper
    except IntegrityError as e:
        print(f"Error creating newspaper: {e}")
        return None


def create_news_article(newspaper):
    """Creates a fake news article entity."""
    try:
        # Fake articles with a random date uploaded (past 180 days)
        date_uploaded = fake.date_between(start_date="-183d", end_date="today")

        article = NewsArticleEntity.create(
            newspaper_id=newspaper.id,
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=50),
            date_uploaded=date_uploaded,
        )
        print(f"Created Article: {article.title} - {article.date_uploaded}")
        return article
    except IntegrityError as e:
        print(f"Error creating article: {e}")
        return None
