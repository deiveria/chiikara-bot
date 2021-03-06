import re
from database import GuildConfig
from discord import Embed
from discord.ext import commands

from helpers import helpers


async def build_config_embed(guild_obj, guild_info):
    embed = Embed(title=guild_obj.name,
                  description='Configurações do servidor, aqui você pode configurar tudo usando os comandos!',
                  colour=0x7BB9FB)

    embed.set_thumbnail(url=guild_obj.icon_url)

    log_channel = bot_channel = "Não configurado"

    if guild_info.bot_channel is not None:
        bot_channel = f'<#{guild_info.bot_channel}>'

    if guild_info.log_channel is not None:
        log_channel = f'<#{guild_info.log_channel}>'

    embed.add_field(name='Canal de bots', value=bot_channel, inline=True)
    embed.add_field(name='Canal de logs', value=log_channel, inline=True)

    return embed


def parse_channel_string(s):
    return re.sub('[<>#]', '', s)


async def set_bot_channel(guild, channel):
    query = guild.update(bot_channel=parse_channel_string(channel))
    query.execute()


async def set_log_channel(guild, channel):
    query = guild.update(log_channel=parse_channel_string(channel))
    query.execute()


# Comandos com utilidade, geralmente de controle do servidor.
class GuildsCommands(commands.Cog, name='Moderação'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='config', aliases=['settings'])
    @commands.guild_only()
    async def config(self, ctx, *args):
        # Pegando as informações da guilda na database
        guild, created = GuildConfig.get_or_create(guild_id=ctx.guild.id)
        # Caso o usuário não tenha dado nenhum paramêtro só vamos exibir as informações
        if len(args) == 0:
            return await ctx.send(embed=await build_config_embed(ctx.guild, guild))
        # Hmm, não sei como fazer isso da maneira certa, vai ser assim.
        option = args[0]
        # Selecionar o canal para bots
        if option == 'bot':
            await set_bot_channel(guild, args[1])
            await ctx.send(embed=helpers.info_embed(f'Prontinho, o canal {args[1]} é o canal de bot agora.'))
        # Selecionar o canal para logs
        elif option == 'log':
            await set_log_channel(guild, args[1])
            await ctx.send(embed=helpers.info_embed(f'Prontinho, o canal {args[1]} é o canal de logs agora.'))
        else:
            pass


def setup(bot):
    bot.add_cog(GuildsCommands(bot))
