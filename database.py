from peewee import *

# Arquivo da database vai ser bot.db, porque sim.
db = SqliteDatabase('bot.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class LastMessage(BaseModel):
    user_id = IntegerField()
    guild = IntegerField()
    message = IntegerField(null=True)
    channel = IntegerField(null=True)
    timestamp = TimestampField(null=True)

    class Meta:
        primary_key = CompositeKey('user_id', 'guild')

def create_tables():
    db.create_tables([LastMessage])


if (__name__ == "__main__"):
    create_tables()
