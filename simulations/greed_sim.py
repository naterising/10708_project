# -*- coding: utf-8 -*-
"""
Script to run a round of Greed
"""

from Player import Player
from MDPPlayer import MDPPlayer
from SimpleGame import SimpleGame
from datetime import datetime
import numpy as np

NUM_ROUNDS = 30
avg_scores = np.zeros((1,2)) # 2 players
p0_wins = 0

for i in range(NUM_ROUNDS):
    # instantiate a list of players
    p0 = Player(0)
    p1 = MDPPlayer(1, policy_filepath='data/policies/policy iteration/policy gamma=0.9 penalty = -10000 farkle penalty.pkl')
    
    players = [p0,p1]
    
    # instantiate a game 
    time = datetime.now()
    time_str = time.strftime('M%m-D%d-H%H_m%M-s%S-%f')[:-3]
    log_file_path  = "data/"+time_str+"_log.log"
    score_data_path = "data/"+time_str+"_scores.csv"
    
    game = SimpleGame(players,log_file_path,score_data_path)
    
    # run the game
    final_scores = game.play_game()
    
    avg_scores += final_scores
    if final_scores[0] > final_scores[1]:
        p0_wins += 1
    
print("Average scores, each player: "+str(avg_scores / NUM_ROUNDS))
print("Player 0 wins: "+str(p0_wins))
print("Player 1 wins: "+str(NUM_ROUNDS-p0_wins))
