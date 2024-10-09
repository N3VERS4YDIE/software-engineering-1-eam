from peewee import AutoField, CharField, IntegerField, Model

from app.db import get_db


class NewspaperEntity(Model):
    id = AutoField()
    name = CharField(max_length=255)
    email = CharField(max_length=320)

    class Meta:
        database = get_db()
        table_name = 'newspapers'
