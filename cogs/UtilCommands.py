import discord
from database import *
from helpers.helpers import info_embed
from discord.ext import commands


# Comandos com utilidade, geralmente de controle do servidor.
class UtilCommands(commands.Cog, name='Utilidade'):

    def __init__(self, bot):
        self.bot = bot

    # Esconder um canal
    @commands.command(name='esconder', aliases=['esconda', 'hide'])
    async def esconder(self, ctx, channel: discord.TextChannel):
        # Pegando o valor na database
        hidden, created = HiddenChannels.get_or_create(user_id=ctx.author.id, channel=channel.id)
        # Se o usuário já tiver escondido antes, o comando será cancelado.
        if not created:
            embed = info_embed("Desculpe, mas você já escondeu esse canal.", level="warning")
            return await ctx.send(embed=embed)
        # Recebendo os overwrites para esse usuário no canal marcado
        overwrite = channel.overwrites_for(ctx.author)
        # Atualizando os valores de ler e escrever no canal para Falso
        overwrite.update(send_messages=False, read_messages=False)
        # Setando os valores definidos
        await channel.set_permissions(ctx.author, overwrite=overwrite)

        embed = info_embed(f'Prontinho, o canal #{channel.name} foi escondido pra você!')
        await ctx.channel.send(embed=embed)

    # Exibir um canal que o usuário escondeu
    # TODO: Verificar se foi mesmo o próprio usuário que escondeu
    @commands.command(name='exibir', aliases=['mostrar', 'show'])
    async def exibir(self, ctx, channel: discord.TextChannel):
        # Pegando o valor na database, porém aqui usando uma função que vai retornar None se não existir.
        hidden = HiddenChannels.get_or_none(user_id=ctx.author.id, channel=channel.id)
        # Se o valor for none, ou self_hidden for False, o comando não será executado.
        if hidden is None or not hidden.self_hidden:
            embed = info_embed("Desculpe, mas você não escondeu esse canal.", level="warning")
            return await ctx.send(embed=embed)
        # Deletando os registros na database.
        hidden.delete_instance()
        # Recebendo os overwrites para esse usuário no canal marcado
        overwrite = channel.overwrites_for(ctx.author)
        # Definindo os valores para None
        overwrite.update(send_messages=None, read_messages=None)
        # Caso os overwrites sejam todos None após remover esses dois, ele vai deletar o overwrite como um todo
        if overwrite.is_empty():
            await channel.set_permissions(ctx.author, overwrite=None)
        # Senão apenas esses dois.
        else:
            await channel.set_permissions(ctx.author, overwrite=overwrite)

        embed = info_embed(f'Prontinho, o canal <#{channel.id}> foi exibido de volta pra você!')
        await ctx.channel.send(embed=embed)

    @esconder.error
    @exibir.error
    async def exibir_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.ChannelNotFound):
            embed = info_embed("Desculpe, não fui capaz de encontrar esse canal.", level="error")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(UtilCommands(bot))
