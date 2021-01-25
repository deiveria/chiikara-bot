import discord
from discord.ext import commands


class MiscCommands(commands.Cog, name='Diversos'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='falar', aliases=['diga', 'say', 'fala'])
    @commands.guild_only()
    async def falar(self, ctx, channel: discord.TextChannel, *, arg):
        await channel.send(arg)

    @falar.error
    async def falar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Não pude encontrar esse canal.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você precisa mandar o canal e a mensagem a ser dita.")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
