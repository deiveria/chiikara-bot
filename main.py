import discord
import os
from discord.ext import commands


client = commands.Bot(command_prefix='.')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.event
async def on_ready():
    print('Logado como {0.user}.'.format(client))


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('NjY3NTA3ODI0MzY4MDI1NjEw.XiDvGw.xOdCadANes0o9H_c-zRdXnosnS8')
