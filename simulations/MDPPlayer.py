# -*- coding: utf-8 -*-
"""
General class defining a player object.

Any player that plays the game will have the same constructor and must implement
two methods that determine their strategy 
"""
import pickle
from Player import Player
import game_utils

class MDPPlayer(Player):
    
    
    def __init__(self,player_num, policy_filepath):
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

        self.policy = {}
        self.value = {}
        with open(policy_filepath, 'rb') as f:
            self.policy = pickle.load(f)

        
    # technically this can be deleted since inherits from Player
    # def update_game_state(self,state):
    #     """
    #     Before a player plays their turn, the Game object will update their game
    #     state by passing in the current state. This is a tuple that encodes:
            
    #     (all player's scores, current roll, accrued pts)
        
    #     """
        
    #     self.all_scores = state[0]
    #     self.num_available_dice = state[1]
    #     self.accrued_score = state[2]
        
    
    def pass_or_roll(self):
        """
        Player decides whether to roll again or pass 
    
        Returns: True if player wants to roll again
        Returns: False if player wants to end their turn
        """

        # very basic flip coin to pass or roll if state is (6,())
        return self.policy[(self.num_available_dice, ())] == 'roll'
        
    
    
    def choose_dice(self):
        """
        Player inspects the current roll.
        If the player has no scoring choices, return [].
        """
        choice = self.policy[(self.num_available_dice, self.current_roll)]
        return choice

        