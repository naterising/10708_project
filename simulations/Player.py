# -*- coding: utf-8 -*-
"""
General class defining a player object.

Any player that plays the game will have the same constructor and must implement
two methods that determine their strategy 
"""

import game_utils

class Player:
    
    
    def __init__(self,game,player_num):
        """
        Initiailize game, passing in @param game to give player access to game state
        """
        self.num_available_dice = 0
        self.current_roll = []
        self.accrued_score = 0
        self.game = game
        
        # each player gets a player number so they can reference other player's scores
        self.player_num = player_num 
        self.all_scores = []
        
        # each player will get updates on the state of the game before they start their turn
        self.state = ()
        
        
        
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
        
        
        # very basic implementation, only keep rolling if you have more than
        # two dice available to roll
        if self.num_available_dice > 2:
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
        
        return best_choice
        