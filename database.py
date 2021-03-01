from peewee import *

# Arquivo da database vai ser bot.db, porque sim.
db = SqliteDatabase('bot.db')
db.connect()


# Modelo Base para as tabelas, indicando para qual database elas pertecem.
class BaseModel(Model):
    class Meta:
        database = db


# Essa tabela armazena as informações sobre a última mensagem enviada pelo usuário.
class LastMessage(BaseModel):
    user_id = IntegerField()
    guild = IntegerField()
    message = IntegerField(null=True)
    channel = IntegerField(null=True)
    timestamp = TimestampField(null=True)

    class Meta:
        primary_key = CompositeKey('user_id', 'guild')


class HiddenChannels(BaseModel):
    user_id = IntegerField()
    channel = IntegerField()
    guild = IntegerField()
    self_hidden = BooleanField(default=True)


def create_tables():
    db.create_tables([LastMessage, HiddenChannels])


# Caso esse arquivo seja executado diretamente as tabelas serão criadas.
if __name__ == "__main__":
    create_tables()
