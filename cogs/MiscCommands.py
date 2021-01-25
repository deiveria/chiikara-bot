import discord
from discord.ext import commands


class MiscCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='falar', aliases=['diga', 'say'])
    async def falar(self, ctx):
        await ctx.send('Teste')
        print(ctx.message)


def setup(bot):
    bot.add_cog(MiscCommands(bot))
