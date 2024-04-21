
# -*- coding: utf-8 -*-
"""
Player class defining an expert player.

THIS CLASS ONLY APPLIES TO A SIMPLIFIED GAME WITH 2 PLAYERS

"""

import game_utils
import pickle
from Player import Player

WIN_THRESHOLD = 10000

class Expert(Player):
    
    
    def __init__(self,player_num):
        """
        Initiailize game, passing in @param game to give player access to game state
        """
        self.num_available_dice = 0
        self.current_roll = []
        self.accrued_score = 0
        
        # each player gets a player number so they can reference other player's scores
        self.player_num = player_num         
        self.all_scores = []
        
        # each player will get updates on the state of the game before they start their turn
        self.state = ()
        
        # This piece only works with two players with player nums 0/1
        self.opp_num = 0
        if player_num == 0:
            self.opp_num = 1
        
        
        
    def update_game_state(self,state):
        """
        Before a player plays their turn, the Game object will update their game
        state by passing in the current state. This is a tuple that encodes:
            
        (all player's scores, current roll, accrued pts)
        
        """
        
        self.all_scores = state[0]
        self.num_available_dice = state[1]
        self.accrued_score = state[2]
        
    
    def pass_or_roll(self):
        """
        Player decides whether to roll again or pass 
    
        Returns: True if player wants to roll again
        Returns: False if player wants to end their turn
        """
        
        assert self.num_available_dice > 0
        assert self.num_available_dice < 7
        
        opp_score = self.all_scores[self.opp_num]
        expert_score = self.all_scores[self.player_num]
        
        if self.num_available_dice > 2:
            return True
        
        elif self.num_available_dice == 2 and self.accrued_score < 1200:
            return True
        
        elif self.num_available_dice == 1 and opp_score > 10000 and opp_score > expert_score:
            return True
        
        else:
            return False
            
    
    def choose_dice(self):
        """
        Player inspects the current roll.
        If the player has no scoring choices, return [].
        """
        
        # very basic greedy strategy, returns the highest possible score 
        # for the current roll        
        choices = game_utils.get_possible_choices(self.current_roll)
        best_choice = game_utils.get_highest_choice(choices)
        
        # if the best choice scores more than 374, keep it (threshold tuned against simple)
        if game_utils.get_score(best_choice) >= 375:
            return best_choice
            
        
        # otherwise, filter possible choices to the shortest length and take the
        # highest scoring of such choices
        shortest_len = 7
        highest_score = 0
        for choice in choices:
            if len(choice) < shortest_len or (len(choice) == shortest_len and game_utils.get_score(choice) > highest_score):
                best_choice = choice
                shortest_len = len(choice)
                highest_score = game_utils.get_score(choice) 
            
            
                
        
        return best_choice
        