import discord
import os
import config
import database
from discord.ext import commands

# Criando tabelas na database
# Obs, eu não sei se a database tá nos conformes
# Mas se funciona, não vou mudar.
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
