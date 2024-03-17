# -*- coding: utf-8 -*-
"""
Script to run a round of Greed
"""

from Player import Player
from SimpleGame import SimpleGame

# instantiate a list of players
p0 = Player(0, policy_filepath='data/policies/policy gamma=0.9.pkl')
p1 = Player(1, policy_filepath='data/policies/policy gamma=0.9.pkl')

players = [p0,p1]

# instantiate a game 
log_file_path  = "data/turnlog.log"
score_data_path = "data/scores.csv"

game = SimpleGame(players,log_file_path,score_data_path)

# run the game
game.play_game()
