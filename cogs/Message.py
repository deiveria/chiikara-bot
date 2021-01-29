import discord
from datetime import datetime, timezone
from database import *
from discord.ext import commands


# Converter o horário pro fuso do Brasil
def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


# Criar um embed com as informações da última mensagem
async def create_message_embed(message, timestamp):
    # Convertendo o horário e formatando para uma String
    time = utc_to_local(timestamp).strftime("%d/%m/%Y às %H:%M")

    embed = discord.Embed(title=f'Última mensagem de {message.author.name}', colour=0x69DBEF)
    embed.add_field(name='Conteúdo', value=message.content, inline=False)
    embed.add_field(name='Horário', value=time)
    embed.set_footer(text='A última mensagem do usuário só é registrada caso o bot esteja online!')
    embed.set_thumbnail(url=message.author.avatar_url)

    return embed


class Message(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Esse evento é chamado em toda mensagem em um canal que o Bot pode ver
    @commands.Cog.listener()
    async def on_message(self, message):
        # Com o contexto da mensagem é possível saber se ela foi o comando
        ctx = await self.bot.get_context(message)
        # Caso o autor da mensagem seja um bot ou a mensagem tenha sido um comando, ela será ignorada.
        if (message.author.bot or ctx.valid or message.guild == None):
            return

        # Tentando criar o registro na database do usuário, senão só dando um get no mesmo
        user, created = User.get_or_create(
            id=message.author.id, username=message.author.name)
        lm, created = LastMessage.get_or_create(
            user_id=message.author.id, guild=message.guild.id)

        # Atualizando os dados.
        lm.channel = message.channel.id
        lm.message = message.id
        lm.timestamp = message.created_at.timestamp()
        lm.save()

    @commands.command(name='lm')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def lm(self, ctx, member: discord.Member):
        try:
            # Select na database pelos dados da última mensagem
            lm = LastMessage.get(user_id=member.id, guild=ctx.guild.id)
            # Get no canal da mensagem
            channel = ctx.guild.get_channel(lm.channel)
            # Fetch na mensagem dentro do canal
            message = await channel.fetch_message(lm.message)
            # Enviando o embed contendo a última mensagem
            await ctx.send(embed=await create_message_embed(message, lm.timestamp))
        except LastMessage.DoesNotExist:
            await ctx.send('Esse membro não tem mensagens no meu registro.')


def setup(bot):
    bot.add_cog(Message(bot))
