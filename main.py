import discord
import os
import config
import logging
import database
from discord.ext import commands

database.create_tables()
client = commands.Bot(command_prefix=config.prefix)


@client.event
async def on_ready():
    print('Logado como {0.user}.'.format(client))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(config.token)
