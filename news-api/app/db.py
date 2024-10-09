from peewee import Model, MySQLDatabase

db = MySQLDatabase(
    "newspapers",
    user="root",
    password="",
    host="localhost",
    port=3306,
)


def get_db():
    if db.is_closed():
        db.connect()
    return db
