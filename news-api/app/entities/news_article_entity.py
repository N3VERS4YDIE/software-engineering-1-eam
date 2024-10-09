from datetime import date

from peewee import AutoField, CharField, DateField, IntegerField, Model, TextField

from app.db import get_db


class NewsArticleEntity(Model):
    id = AutoField()
    newspaper_id = IntegerField()
    title = CharField(max_length=255)
    content = TextField()
    date_uploaded = DateField(default=date.today)

    class Meta:
        database = get_db()
        table_name = "news_articles"
