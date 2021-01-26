import discord
import helpers.anilist as anilist
from discord.ext import commands


class AnimeCommands(commands.Cog, name='Anime e Mangá'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='anime')
    async def anime(self, ctx, *, anime_name):
        await ctx.send(embed=anilist.anime(anime_name))

    @anime.error
    async def anime_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você não enviou nenhum argumento.")


def setup(bot):
    bot.add_cog(AnimeCommands(bot))
