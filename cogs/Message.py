import discord
from time import time
from database import *
from discord.ext import commands


class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Caso o autor da mensagem seja um bot ele será ignorado
        if (message.author.bot):
            return
        # Insert na tabela User caso o mesmo não exista.
        user, created = User.get_or_create(
            id=message.author.id, username=message.author.name)
        # Mesma coisa, mas agora para a LastMessage
        lm, created = LastMessage.get_or_create(
            user_id=message.author.id, guild=message.guild.id)

        # Atualizando os dados.
        lm.channel = message.channel.id
        lm.message = message.id
        lm.timestamp = time()
        lm.save()


def setup(bot):
    bot.add_cog(Message(bot))
