import os

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = os.getenv('COMMAND_PREFIX')
STATS_CHANNEL = os.getenv('STATS_CHANNEL')

STATS_TEMPLATE = '''

**Least:**

**Most:**

'''

LEAST_HEADER = '**Least:**'
MOST_HEADER = '**Most:**'

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

pin = None

least = {}
most = {}


def check_channel(channel):
    return channel.name == STATS_CHANNEL


def parse_line(line):
    parts = line.split(': ')
    tail_parts = parts[1].split(' ')
    kills = parts[0]
    damage = tail_parts[0]
    player = ''
    if len(tail_parts) > 1:
        player = tail_parts[1]
    return kills, damage, player


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Listening on channel {STATS_CHANNEL}')

    channel = discord.utils.get(bot.guilds[0].text_channels, name=STATS_CHANNEL)

    pins = await channel.pins()

    global pin
    pin = discord.utils.get(pins, author=bot.user)
    if pin is None:
        message = await channel.send(STATS_TEMPLATE)
        await message.pin()
        pin = message
    else:
        lines = pin.content.splitlines()
        ind_least = lines.index(LEAST_HEADER)
        ind_most = lines.index(MOST_HEADER)
        least_lines = lines[(ind_least + 1):(ind_most - 1)]
        most_lines = lines[(ind_most + 1):(len(lines) - 1)]
        for line in least_lines:
            kills, *tail = parse_line(line)
            least[kills] = tail

        for line in most_lines:
            kills, *tail = parse_line(line)
            most[kills] = tail


@bot.command(name='stats', help='show current stats')
async def stats(ctx):
    if not check_channel(ctx.channel):
        return
    await ctx.send(pin.content)


bot.run(TOKEN)
