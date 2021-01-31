import discord
from discord.ext import commands


# Comandos em geral. Geralmente não tem uma utilidade grande, são apenas coisas aleatórias.
class MiscCommands(commands.Cog, name='Diversos'):

    def __init__(self, bot):
        self.bot = bot

    # Comando para o bot dizer em algum canal alguma mensagem específicada pelo usuário
    @commands.command(name='falar', aliases=['diga', 'say', 'fala', 'fale'])
    @commands.guild_only()
    async def falar(self, ctx, channel: discord.TextChannel, *, text):
        await channel.send(text)

    # Comando para pegar o avatar de algum membro do servidor, é necessário marcar ou dizer o nome.
    @commands.command(name='avatar', aliases=['foto', 'icon', 'pfp'])
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member):
        avatar_link = member.avatar_url_as(format='png', static_format='webp', size=2048)
        avatar_embed = discord.Embed(title=f"Avatar - {member.name}#{member.discriminator}", colour=0xEE4D4D)
        avatar_embed.set_image(url=avatar_link)
        await ctx.send(embed=avatar_embed)


def setup(bot):
    bot.add_cog(MiscCommands(bot))
