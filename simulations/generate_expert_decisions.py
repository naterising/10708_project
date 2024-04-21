# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 14:10:00 2024

@author: nater
"""
from Expert import Expert
import random
import numpy as np
import pandas as pd


def get_action_number():
    """
    Return 0 with prop .5, 1 with prob .5
    """
    p = random.random()
    if p <= 0.5:
        return 0
    else:
        return 1
    
def get_banked_score():
    """
    Returns a number 0 to 11000
    
    If the score is over 10000, resample until a score less than 10000
    is reached with probability 0.5
    
    """
    
    n = random.randint(0, 11000)
    p = random.random()
    
    if n > 10000 and p > .5:
        n = random.randint(0,10000)
        
    return round(n / 50) * 50


def get_dice_num():
    """
    Generates a number between 1 and 6 (inclusive)
    
    Can be used to represent the number of dice available to roll or the
    value a dice takes on

    """
    return random.randint(1,6)

def get_accrued_score():
    """
    Generates a value for the accrued score.
    1. Choose a bucket with some probability
    2. Randomly pick a number from that bucket
    """
    
    p = random.random()
    
    # pull from [50,1000]
    if p <= .3:
        lo = 0
        hi = 0
    
    elif p <= .72: 
        lo = 50
        hi = 1000
        
    # pull from [1000,2000]
    elif p <= 0.895: 
        lo = 1000
        hi = 2000
        
    # pull from [2000,5000]
    elif p <= 0.965:
        lo = 2000
        hi = 5000
        
    # pull from [5000,10000]
    else:
        lo = 5000
        hi = 10000
        
    return round(random.randint(lo,hi) / 50) * 50
        




NUM_SAMPLES = 10
expert = Expert(0)

# generate random states
data = []
for i in range(NUM_SAMPLES):
    # randomly sample a game state
    action = get_action_number()
    player_score = get_banked_score()
    opp_score = get_banked_score()
    accrued_score = get_accrued_score()
    num_dice = get_dice_num()
    dice = list(np.zeros(6).astype(int))
    
    # simulate a dice roll if action is to choose dice
    if action == 1: 
        
        # if the number of dice to choose from for an action=1, resample until
        # you get num dice > 1. This is becuase this decision is deterministic
        while num_dice == 1:
            num_dice = get_dice_num()
        
        for j in range(num_dice):
            dice[j] = get_dice_num()
            
            
    # now, all state information is initialized. Need to determine outcome.
    # First load simulated params into the expert's state
    expert.num_available_dice = num_dice
    expert.accrued_score = accrued_score
    expert.all_scores = [player_score, opp_score]
    
    # pass/roll action
    if action == 0:
        outcome = expert.pass_or_roll()
        if outcome == True:
            outcome = [1,0,0,0,0,0]
        else:
            outcome = [0,0,0,0,0,0]
        
    # choose dice action    
    else:
        sorted_dice = [x for x in dice if x != 0]
        expert.current_roll = tuple(sorted(sorted_dice))
        choice = expert.choose_dice()
        
        outcome = [0,0,0,0,0,0]
        for c in choice:
            for d in range(len(dice)):
                if dice[d] == c and outcome[d] == 0:
                    outcome[d] = 1
                

    sample = [action, player_score, opp_score, accrued_score, num_dice, dice[0], dice[1], dice[2], dice[3],dice[4],dice[5], outcome]
    data.append(sample)


columns = ["Action", "PlayerScore","OpponentScore","AccruedScore","NumDiceAvailable","Dice1","Dice2","Dice3","Dice4","Dice5","Dice6","Outcome"]
df = pd.DataFrame(data,columns=columns)




