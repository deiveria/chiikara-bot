from peewee import *

# Arquivo da database vai ser bot.db, porque sim.
db = SqliteDatabase('bot.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = TextField(null=True)


class LastMessage(BaseModel):
    user = ForeignKeyField(User, backref='lastmessage')
    guild = IntegerField()
    message = IntegerField(null=True)
    channel = IntegerField(null=True)
    timestamp = TimestampField(null=True)


def create_tables():
    db.create_tables([User, LastMessage])


if (__name__ == "__main__"):
    create_tables()
