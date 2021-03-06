from helpers.helpers import info_embed
from difflib import get_close_matches
from discord.ext import commands


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Esse evento é chamado em todos os erros relacionados a execução de um comando.
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Caso o erro seja o comando não ser encontrado
        if isinstance(error, commands.CommandNotFound):
            # O que você digitado ao tentar acessar o comando
            sent_cmd = ctx.invoked_with
            # Lista de todos os nomes dos comandos
            cmds = []
            for cmd in self.bot.commands:
                # Comandos marcados como hidden não serão mostrados
                if cmd.hidden:
                    continue
                # Adicionado o nome de cada comando à lista
                cmds.append(cmd.name)
                # Adicionando também seus aliases
                cmds.extend(cmd.aliases)
            # Comandos que tem nomes parecidos com o que foi digitado
            matches = get_close_matches(sent_cmd, cmds)
            # Caso ele encontre algum comando que seja próximo, será enviado ao usuário a dica
            if len(matches) > 0:
                embed = info_embed(
                    f'O comando "**{sent_cmd}**" não foi encontrado, você quis dizer "**{matches[0]}**"?',
                    level='info'
                )
                await ctx.send(embed=embed)
            # Senão irá apenas avisar que não existe tal comando.
            else:
                embed = info_embed(
                    f'O comando"**{sent_cmd}**" não foi encontrado, use o comando **"ajuda"** para saber mais.',
                    level='warning'
                )
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
