
# bot.py
import os
import random
import discord
from helper import *
from SPLhelper import *
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #app token
CHANNEL = os.getenv('CHANNEL_NAME') #channel name to interact with the bot
R_ACTIVE = os.getenv('REWARD_ACCOUNT_ACTIVE_KEY') #reward account active key for auto-reward distribution
R_POSTING = os.getenv('REWARD_ACCOUNT_POSTING_KEY') #reward accont posting key for auto-reward distribution

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!',intents = intents)

@bot.event
async def on_ready(): #this method happens upon initialization of the bot
    print(f'{bot.user.name} has connected to Discord!\n'
            f'{bot.user.name} is connected to the following guild(s):\n')
    for g in bot.guilds:
        print(f'{g.name}(id: {g.id})')
        members = '\n'
        for member in g.members:
            members =  members + '-' + member.name + '\n'
        print(f'Guild Members: {members}')
    print('Initialized - awaiting events...')

@bot.event
async def on_message(message): #occurs when a new message is typed
    if message.author == bot.user:
        return #if bot is seeing its own message, ignore
    if message.channel.name != CHANNEL:
        return #if message is NOT in "pwnd-bot" channel, ignore
    if message.content == 'ping':
        await message.channel.send('pong - on_message')
    await bot.process_commands(message) #sends commands to the commands methods after through this one

@bot.command(name="add_Brawl", help='*** {cycle} - Add the brawl results and tally points for given brawl cycle. (***Officers only)')
@commands.has_role('Officers')
async def add_Brawl(ctx, cycle: int):
    log(f'ADDING BRAWL POINTS FOR BRAWL CYCLE {cycle}')
    await message_splicer_sender(ctx, recordBrawl(ctx, cycle, True)) #function, should return string
    updateBrawlCycleNumber(cycle)

@bot.command(name="remove_Brawl", help='*** {cycle} - Subtract the brawl results and tally points for given brawl cycle.  (***Officers only)')
@commands.has_role('Officers')
async def remove_Brawl(ctx, cycle: int):
    log(f'REMOVING BRAWL POINTS FOR BRAWL CYCLE {cycle}')
    await message_splicer_sender(ctx, recordBrawl(ctx, cycle, False)) #function, should return string
    # await ctx.send(recordBrawl(ctx, cycle, False)) 

@bot.command(name="check_Brawl", help='*** - Return the most recent brawl cycle added.  (***Officers only)')
@commands.has_role('Officers')
async def check_Brawl(ctx):
    await message_splicer_sender(ctx, checkBrawl(ctx)) #function, should return string
    # await ctx.send(recordBrawl(ctx, cycle, False)) 

@bot.command(name="change_Log", help='*** {} - Show the last 99 lines from the changelog. (***Officers only)')
@commands.has_role('Officers')
async def change_Log(ctx):
    await message_splicer_sender(ctx,display_log(99)) # calls helper function, should return string
    #await ctx.send(display_log(99)) 

@bot.command(name="change_Log_N", help='*** {num} - Show the last N lines from the changelog. (***Officers only)')
@commands.has_role('Officers')
async def change_Log_N(ctx, lines: int):
    await message_splicer_sender(ctx, display_log(lines)) # calls helper function, should return string
    #await ctx.send(display_log(lines)) 

@bot.command(name="change_Log_Name", help='*** {@name} - Show the last 99 lines from the changelog for specific user. (***Officers only)')
@commands.has_role('Officers')
async def change_Log_Name(ctx, user: str):
    await message_splicer_sender(ctx,display_log_user(ctx, user, 99)) # calls helper function, should return string

@bot.command(name="change_Log_Name_N", help='*** {@name, num} - Show the last N lines from the changelog for specific user. (***Officers only)')
@commands.has_role('Officers')
async def change_Log_Name_N(ctx, user: str, lines: int):
    await message_splicer_sender(ctx,display_log_user(ctx, user, lines)) # calls helper function, should return string
    #await ctx.send(display_log_user(ctx, user, lines)) 

@bot.command(name="add_Points", help='*** {@name, num} - Add or subtract (with negative value) point value from a specific user. (***Officers only)')
@commands.has_role('Officers')
async def add_Points(ctx,user: str, points: int):
    # this one should always only be 1 line, dont need splicer method here
    await ctx.send(add_points(ctx, user, points,'')) # calls helper function, should return string

@bot.command(name="ping", help='{} Heartbeat to verify if the bot is running correctly.')
async def ping(ctx):
    #user = '<@876552577079197727>'
    #await ctx.send(f'pong for {user}')
    #await ctx.send('pong for <@1175587765203767317>')
    await ctx.send('pong')

@bot.command(name='display_All', help='{} Displays the current points table.')
async def display_all(ctx):
    await message_splicer_sender(ctx,display_points_all())
    #await ctx.send(display_points_all())

@bot.command(name='display_Name', help='{@name} Displays a specific user\'s current points.')
async def display_name(ctx, user):
    # this one should always only be 1 line, dont need splicer method here
    await ctx.send(display_points(ctx, user))

#split lines of a message up into chunks of 18 lines each.
async def message_splicer_sender(ctx, msg):
    lines = msg.split('\n')
    limit = 18
    if len(lines) < limit:
        await ctx.send(msg)
    else:
        #split into multiple messages
        m = []
        x = 0
        for i in range(0, len(lines)):
            m.append(lines[i])
            x = x+1
            if x == limit:
                x=0
                await ctx.send('\n'.join(m))
                m = []
        if m != []:
            await ctx.send('\n'.join(m)) #send leftovers if they exist

#error handling
@bot.event
async def on_error(event, *args, **kwards):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else: 
            raise

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('Only Officers may run this command.')

#testings methods, don't need anymore
#@bot.command(name='roll_dice', help='Simulate a dice roll.')
#@commands.has_role('Officers')
#async def roll_dice(ctx, number_of_dice: int, number_of_sides: int):
#    dice = [ str(random.choice(range(1, number_of_sides +1)))
#            for _ in range(number_of_dice)]
#    await ctx.send(', '.join(dice))

bot.run(TOKEN)