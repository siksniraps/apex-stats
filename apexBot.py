import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
STATS_CHANNEL = os.getenv('STATS_CHANNEL')

bot = commands.Bot(command_prefix=COMMAND_PREFIX)


def check_channel(channel):
    return channel.name == STATS_CHANNEL


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Listening on channel {STATS_CHANNEL}')

    channel = discord.utils.get(bot.guilds[0].text_channels, name=STATS_CHANNEL)

    pins = await channel.pins()

    pin = discord.utils.get(pins, author=bot)
    if pin is None:
        message = await channel.send('stats')
        message.pin()


@bot.command(name='stats', help='show current stats')
async def stats(ctx):
    if not check_channel(ctx.channel):
        return
    await ctx.send('stats')


bot.run(TOKEN)
