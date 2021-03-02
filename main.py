import os
import config
import sys
import database
from discord.ext import commands

# Checando se a token foi colocada.
if config.token == "SUA TOKEN AQUI":
    sys.exit("Você não configurou sua token no config.py")

# Criando tabelas no banco da dados
database.create_tables()

# Inicando o client usando o módulo de comandos
client = commands.Bot(command_prefix=config.prefix)


# Esse evento é chamado quando o bot fica online
@client.event
async def on_ready():
    print('Logado como {0.user}.'.format(client))


# Para cada arquivo .py em ./cogs ele vai tentar carregar a classe
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Logando no bot.
client.run(config.token)
