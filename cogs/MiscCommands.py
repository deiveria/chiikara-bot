import discord
from discord.ext import commands


class MiscCommands(commands.Cog, name='Diversos'):

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name='avatar')
    @commands.guild_only()
    async def avatar(self, ctx, member: discord.Member):
        avatar_link = member.avatar_url_as(
            format='png', static_format='webp', size=2048)
        avatar_embed = discord.Embed(
            title=f"Avatar - {member.name}#{member.discriminator}", colour=0xEE4D4D)
        avatar_embed.set_image(url=avatar_link)
        await ctx.send(embed=avatar_embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Membro não encontrado.")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
