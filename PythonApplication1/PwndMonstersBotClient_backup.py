
# bot.py
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents = intents)


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    #guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    #for guild in client.guilds:
    #    if guild.name == GUILD:
    #        break

    print(
        f'{client.user} has connected to Discord!\n'
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
        )

    members = ''
    for member in guild.members:
        members =  members + '\n -' + member.name

    
    print(f'Guild Members:\n - {members}')
    print('Initialized - awaiting events...')

@client.event
async def on_message(message):
    if message.author == client.user:
        return #if bot is seeing its own message, ignore
    
    if message.channel.name != 'pwnd-bot':
        return #if message is NOT in "pwnd-bot" channel, ignore

    #officer powers

    #everyone powers
    
    if message.content == 'ping':
        await message.channel.send('pong')

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content== '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwards):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else: 
            raise

client.run(TOKEN)