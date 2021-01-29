import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingPermissions


class MiscCommands(commands.Cog, name='Diversos'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='falar', aliases=['diga', 'say', 'fala', 'fale'])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def falar(self, ctx, channel: discord.TextChannel, *, text):
        await channel.send(text)

    @falar.error
    async def falar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Você não marcou nenhum canal.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você precisa mandar o canal e a mensagem a ser dita.")
        if isinstance(error, commands.MissingPermissions):
            return

    @commands.command(name='avatar', aliases=['foto', 'icon', 'pfp'])
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
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Você não marcou nenhum usuário.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Membro não encontrado.")


def setup(bot):
    bot.add_cog(MiscCommands(bot))
