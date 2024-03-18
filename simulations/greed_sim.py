# -*- coding: utf-8 -*-
"""
Script to run a round of Greed
"""

from Player import Player
from MDPPlayer import MDPPlayer
from SimpleGame import SimpleGame
from datetime import datetime

NUM_ROUNDS = 3

for i in range(NUM_ROUNDS):
    # instantiate a list of players
    p0 = Player(0)
    p1 = MDPPlayer(1, policy_filepath='../data/policies/policy gamma=0.9.pkl')
    
    players = [p0,p1]
    
    # instantiate a game 
    time = datetime.now()
    time_str = time.strftime('M%m-D%d-H%H_m%M-s%S-%f')[:-3]
    log_file_path  = "data/"+time_str+"_log.log"
    score_data_path = "data/"+time_str+"_scores.csv"
    
    game = SimpleGame(players,log_file_path,score_data_path)
    
    # run the game
    final_scores = game.play_game()
    
    print(final_scores)
