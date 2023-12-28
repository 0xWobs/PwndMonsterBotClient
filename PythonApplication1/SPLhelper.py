import json
import requests
import random
import string
import os
import discord
from beem.transactionbuilder import TransactionBuilder
from beembase.operations import Custom_json
from helper import *
from dictionaries import ign_d
from dictionaries import d_ign
from dictionaries import tier3_bonus
from dictionaries import tier4_bonus

pwndID = 'c43af991dc15970e2047548f5b7bfc30a9943543'
#this file is to put Splinterlands API calls and interactions here

#Add Brawl Data To Users
#cycle should be cycle number,
#toAdd is BOOL whether to Add (true) or Subtract (false) scores
def recordBrawl(ctx, cycle, toAdd):
    #first step - identify the tournament ID based on the cycle number and guild ID
    t_ID = ''
    try:
        r = requests.get(f'https://api.splinterlands.com/guilds/brawl_records?guild_id={pwndID}&cycle={cycle}')
        jsonData = json.loads(r.text)
        t_ID = jsonData['results'][0]['tournament_id']
    except Exception as e:
        return f'Error trying to find the Tournament ID from guilds/brawl_records! \n {e}'

    output = []
    #second step - pull json brawl data
    try:
        r = requests.get(f'https://api.splinterlands.com/tournaments/find_brawl?id={t_ID}&guild_id={pwndID}')
        jsonData = json.loads(r.text)
        #iterate through players and record results
        for p in jsonData['players']:
            battles_entered = p['entered_battles']
            wins = p['wins']
            losses = p['losses']
            draws = p['draws']
            name = p['player']
            fray = p['fray_index']
            brawl = p['brawl_level']
            output.append(calculatePoints(ctx, name, battles_entered, wins, losses, draws, fray, brawl, cycle, toAdd))
    except Exception as e:
        return f'Error trying to find the brawl data from /tournaments/find_brawl records! \n {e}'

    return '\n'.join(output) #returns the messages back, one line per user

def calculatePoints(ctx, name, battles_entered, wins, losses, draws, fray, brawl, cycle, toAdd):
    memo = name
    if battles_entered == 0: #TODO, this does not work and will never trigger. even with surrenders battles entered will match how many battles there were
        idk = ign_d['idkpdx']
        return f'User {ign_d[name]} did NOT enter battles for brawl cycle {cycle}. {idk}'
    total = 0
    #current algorithm = 1 point per win and half point for draws
    total = total + wins
    memo = f'{memo} +{wins} for wins,'
    if draws > 0:
        total = total + (0.5*draws)
        memo = f'{memo} +{draws} for draws (half points),'
    
    #3 bonus points for 0 losses, 1 bonus point for 1 loss
    if losses == 0:
        total = total + 3
        memo = f'{memo} +3 for no losses,'
    elif losses == 1:
        total = total + 1
        memo = f'{memo} +1 for only 1 loss,'
    #bonus points for tougher fray assignemnts
    fray_bonus = 0
    if brawl == 6:
        fray_bonus = tier3_bonus[str(fray)]        
    elif brawl == 8:
        #TODO need to check this!! not sure this is corrrect
        fray_bonus = tier4_bonus[str(fray)]
    else:
        #todo??
        return f'HELP not sure what to do here, unexpected brawl value in calculatePoints {brawl}'

    #adding condition to fray bonus algorithm - user must win at least 1 battle to earn fray bonus.  assuming more than 2 battles possible, 0/1, and 0/2 still earns fray difficulty bonus but above that requires at least 1 win.
    if battles_entered > 2:
        # more than 2 battles, must have at least 1/3 or better to earn fray bonus
        if wins > 0:
            total = total + fray_bonus
            memo = f'{memo} and +{fray_bonus} for fray difficulty. +{total} total.'
        else:   
            #fray bonus lost, no wins.
            memo = f'{memo} and +0 for fray difficulty(no wins). +{total} total.'
    else:
        #less than 2 battles, ignore extra condition
        total = total + fray_bonus
        memo = f'{memo} and +{fray_bonus} for fray difficulty. +{total} total.'

    if toAdd == False:
        total = total * -1 #if needed to delete points from a brawl added erroniously or doubled then do so here

    return(add_points(ctx,ign_d[name],total,memo))