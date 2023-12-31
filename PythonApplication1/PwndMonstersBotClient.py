
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
R_NAME = 'wobs4'
R_ACTIVE = os.getenv('REWARD_ACCOUNT_ACTIVE_KEY') #reward account active key for auto-reward distribution
R_POSTING = os.getenv('REWARD_ACCOUNT_POSTING_KEY') #reward accont posting key for auto-reward distribution

BUY_REBELLION_POINTS = 50 #cost in points
BUY_REBELLION_TOKENS = 1 #tokens earned for the points
BUY_SPS_POINTS = 25 # point cost to purchase sps
BUY_SPS_TOKENS = 40 #sps earned 
BUY_DEC_POINTS = 15 #point cost to purchase dec
BUY_DEC_TOKENS = 1000 #tokens earned for the points

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

@bot.command(name="change_Log", help='{} - Show the last 99 lines from the changelog. (***Officers only)')
#@commands.has_role('Officers')
async def change_Log(ctx):
    await message_splicer_sender(ctx,display_log(99)) # calls helper function, should return string
    #await ctx.send(display_log(99)) 

@bot.command(name="change_Log_N", help='{num} - Show the last N lines from the changelog. (***Officers only)')
#@commands.has_role('Officers')
async def change_Log_N(ctx, lines: int):
    await message_splicer_sender(ctx, display_log(lines)) # calls helper function, should return string
    #await ctx.send(display_log(lines)) 

@bot.command(name="change_Log_Name", help='{@name} - Show the last 99 lines from the changelog for specific user. (***Officers only)')
#@commands.has_role('Officers')
async def change_Log_Name(ctx, user: str):
    await message_splicer_sender(ctx,display_log_user(ctx, user, 99)) # calls helper function, should return string

@bot.command(name="change_Log_Name_N", help='{@name, num} - Show the last N lines from the changelog for specific user. (***Officers only)')
#@commands.has_role('Officers')
async def change_Log_Name_N(ctx, user: str, lines: int):
    await message_splicer_sender(ctx,display_log_user(ctx, user, lines)) # calls helper function, should return string
    #await ctx.send(display_log_user(ctx, user, lines)) 

@bot.command(name="add_Points", help='*** {@name, num} - Add or subtract (with negative value) point value from a specific user. (***Officers only)')
@commands.has_role('Officers')
async def add_Points(ctx,user: str, points: int):
    # this one should always only be 1 line, dont need splicer method here
    await ctx.send(add_points(ctx, user, points,'')) # calls helper function, should return string

@bot.command(name="ping", help='{} Heartbeat to verify if the bot is running.')
async def ping(ctx):
    #user = '<@876552577079197727>'
    #await ctx.send(f'pong for {user}')
    #await ctx.send('pong for <@1175587765203767317>')
    await ctx.send('pong')

    #this works too
    #await ctx.send('type yes up for pong')
    #def check(m):
    #    return m.author == ctx.author
    #try:
    #    msg = await bot.wait_for('message', timeout=5.0, check=check)
    #    if msg.content == 'yes':
    #        await ctx.send('pong')
    #    else:
    #        await ctx.send('failure')
    #except asyncio.TimeoutError:
    #    await ctx.send('Timeout, no response')


    #this works 
    #await ctx.send('thumbs up for pong')
    #def check(reaction, user):
    #    return user == ctx.author and str(reaction.emoji) == '👍'
    #try:
    #    reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    #except asyncio.TimeoutError:
    #    await ctx.send('👎')
    #else:
    #    await ctx.send('👍')
    

@bot.command(name='display_All', help='{} Displays the current points table.')
async def display_all(ctx):
    await message_splicer_sender(ctx,display_points_all())
    #await ctx.send(display_points_all())

@bot.command(name='display_Name', help='{@name} Displays a specific user\'s current points.')
async def display_name(ctx, user):
    # this one should always only be 1 line, dont need splicer method here
    await ctx.send(display_points(ctx, user))

@bot.command(name='display_Rewards', help='{} Displays currently available rewards in the rewards account for purchase.')
async def display_rewards(ctx):
    # this one should always only be 1 line, dont need splicer method here
    await message_splicer_sender(ctx, printAccountBalances(R_NAME))

@bot.command(name='display_Prices', help='{} Displays costs and rewards available for purchase.')
async def display_rewards(ctx):
    # this one should always only be 1 line, dont need splicer method here
    o1 = f'Reward account has the following rewards available:\n'
    o2 = printAccountBalances(R_NAME) + '\n'
    o3 = f'Rebellion Packs cost {BUY_REBELLION_POINTS} points for {BUY_REBELLION_TOKENS} {tknRebellionPacks[1]}\n'
    o4 = f'SPS tokens cost {BUY_SPS_POINTS} points for {BUY_SPS_TOKENS} {tknSPS[1]}\n'
    o5 = f'DEC tokens cost {BUY_DEC_POINTS} points for {BUY_DEC_TOKENS} {tknDEC[1]}\n'
    await message_splicer_sender(ctx,o1+o2+o3+o4+o5)

@bot.command(name='buy_Rebellion', help='{} Purchase a Rebellion pack with points.')
async def buy_Rebellion(ctx):
    discordName = ctx.author.name
    await message_splicer_sender(ctx, await purchaseToken(ctx, R_NAME, R_ACTIVE, discordName, swap_discord_name_for_ign(discordName), BUY_REBELLION_POINTS, tknRebellionPacks[0], BUY_REBELLION_TOKENS))

@bot.command(name='buy_SPS', help='{} Purchase SPS with points.')
async def buy_SPS(ctx):
    discordName = ctx.author.name
    await message_splicer_sender(ctx, await purchaseToken(ctx, R_NAME, R_ACTIVE, discordName, swap_discord_name_for_ign(discordName), BUY_SPS_POINTS, tknSPS[0], BUY_SPS_TOKENS))

@bot.command(name='buy_DEC', help='{} Purchase DEC with points.')
async def buy_DEC(ctx):
    discordName = ctx.author.name
    await message_splicer_sender(ctx, await purchaseToken(ctx, R_NAME, R_ACTIVE, discordName, swap_discord_name_for_ign(discordName), BUY_DEC_POINTS, tknDEC[0], BUY_DEC_TOKENS)) 

#generic method to handle point deduction and token transfer for any purchases
#ctx - the discord context
#rewName - the SPL account name of the reward account to withdraw from
#rewActive - the SPL Active Key for the rewName account
#discordName - the discord member name
#splName - the SPL account name to send the rewards to
#pointSpent - the amount of points to deduct from the receiver
#tokenName - the SPL token name 
#tokenAmount - the SPL token amount to send
async def purchaseToken(ctx, rewName, rewActive, discordName, splName, pointSpent, tokenName, tokenAmount):
    # check user Points Available
    userPoints = get_User_Points(ctx, discordName)
    if userPoints < pointSpent:
        return f'User {discordName} does not have enough points available to purchase {tokenName}. You have {userPoints}, you need {pointSpent} for this purchase. No changes made.'

    # check reward account Tokens available
    rewTokens = getTokenAmount(rewName, tokenName)
    if rewTokens == None:
        return f'Problem getting token balances. Please try again. No changes made.'
    if rewTokens < tokenAmount:
        o1 = f'Reward account does not have enough {tokenName} for this purchase.  Choose something else or ask the Officers for help. Rewards available:'
        o2 = printAccountBalances(rewName)
        return f'{o1}\n{o2}'

    # if both checks passed, proceed with purchase.
    await ctx.send(f'{discordName} is spending  {pointSpent} points to send {tokenAmount} {tokenName} to Splinterlands account: {splName}\nType "yes" to confirm.\nType anything else, or wait 20 seconds, to cancel.')
    def check(m):
        return m.author == ctx.author #inline function to make sure no OTHER user can interrupt the purchase
    try:
        msg = await bot.wait_for('message', timeout=20.0, check=check)
        if msg.content == 'yes':
            #confirmation received, deduct points and broadcast transaction
            output = add_points(ctx, discordName, pointSpent *-1, f'{discordName} is purchasing {tokenName} with {pointSpent} points.')
            output2 = tokenTransfer(rewName, rewActive, splName, tokenName, tokenAmount)
            return f'{output}\n{output2}' # return 
        else:
            #user typed "no" or anything else that is not exactly "yes"
            await ctx.send(f'{discordName} transaction canceled. No changes made.')
    except asyncio.TimeoutError:
        await ctx.send(f'{discordName} transaction timeout. No changes made.')

#split lines of a message up into chunks of 18 lines each.
async def message_splicer_sender(ctx, msg):
    if msg == None:
        return
    lines = msg.split('\n')
    limit = 10
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