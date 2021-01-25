import discord
from discord.ext import commands


"""
Legenda:
[] = Variável do código
{} = Argumento do comando

"""


class MiscCommands(commands.Cog, name='Diversos'):

    def __init__(self, bot):
        self.bot = bot

    """
    Comando para o bot falar certo texto em um canal.

    Argumentos:
    Canal - Mention, nome do canal.
    Texto - Mensagem a ser enviada

    Modo de usar:
    [prefix]falar {Canal} {Texto}

    """

    @commands.command(name='falar', aliases=['diga', 'say', 'fala'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def falar(self, ctx, channel: discord.TextChannel, *, arg):
        await channel.send(arg)

    @falar.error
    async def falar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Você não marcou nenhum canal.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você precisa mandar o canal e a mensagem a ser dita.")

    """
    Comando para buscar o avatar do membro marcado ou digitado.

    Argumentos:
    Membro - Mention, nickname ou username.

    Modo de usar:
    [prefix]avatar {Membro}

    """

    @commands.command(name='avatar')
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member):
        await ctx.send(member.avatar_url_as(format='png', static_format='webp', size=2048))

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Membro não encontrado.")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
