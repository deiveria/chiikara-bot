import discord
from helpers import helpers
from database import *
from discord.ext import commands


# Criar um embed com as informações da última mensagem
async def create_message_embed(message, timestamp):
    # Convertendo o horário e formatando para uma String
    time = helpers.utc_to_local(timestamp).strftime("%d/%m/%Y às %H:%M")

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
        if message.author.bot or ctx.valid or message.guild is None:
            return

        # Tentando criar o registro na database de mensagens, senão só dando um get no mesmo
        lm, created = LastMessage.get_or_create(user_id=message.author.id, guild=message.guild.id)

        # Logando só por motivos de Debug.
        if created:
            s = f"Criado o registro do usuário '{message.author.name}' na guilda '{message.guild.name}'"
            print(s)

        # Atualizando os dados.
        query = lm.update(channel=message.channel.id, message=message.id, timestamp=message.created_at.timestamp())
        query.execute()

    @commands.command(name='lm', aliases=['last', 'msg', 'lmsg'])
    @commands.guild_only()
    async def lm(self, ctx, member: discord.Member):
        # Select na database pelos dados da última mensagem
        lm = LastMessage.get_or_none(user_id=member.id, guild=ctx.guild.id)

        # get_or_none returna o registro do usuário caso ele existe, senão retorna None
        if lm is None:
            embed = helpers.info_embed('Esse membro não tem mensagens no meu registro.', level="error")
            return await ctx.send(embed=embed)

        # Get no canal da mensagem
        channel = ctx.guild.get_channel(lm.channel)
        # Fetch na mensagem dentro do canal
        message = await channel.fetch_message(lm.message)
        # Enviando o embed contendo a última mensagem
        await ctx.send(embed=await create_message_embed(message, lm.timestamp))

    @lm.error
    async def lm_error(self, ctx, error):
        # Acho que essa é a melhor aproximação, pois independente do erro, previsto ou não, vai avisar ao usuário.
        embed = None

        if isinstance(error, commands.MemberNotFound):
            embed = helpers.info_embed('Não foi possível encontrar este membro.', level="error")

        if embed is None:
            embed = helpers.info_embed('Ocorreu um erro que eu não previa, hmm. Tente novamente.', level="error")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Message(bot))
