# -*- coding: utf-8 -*-
"""
Implements a simplified game class for running a Greed simulation:
- points don't carry over from one player to another
- each player starts their turn with 6 die available to roll and 0 pts accrued
- first player to 10000 pts wins (other players don't get one final turn)

"""
import random
import game_utils

WIN_THRESHOLD = 10000

class SimpleGame:
    
    
    def __init__(self, players):
        """
        Each game 
        
        At the start, a list of players is passed to the game.
        These players will play the game in the order they 
        appear in the list.

        """
        
        self.players = players
        self.scores = [0 for i in range(len(players))]
        self.current_roll = [] # initially no dice have been rolled
        self.num_available_dice = 6
        self.accrued_score = 0
        
    def pack_game_state(self):
        return (self.scores, self.num_available_dice, self.accrued_score)
    
    def roll_dice(n):
        """
        Rolls n dice
        """
        possible_values = [1,2,3,4,5,6]
        
        roll = []
        for i in range(n):
            roll.append(random.choice(possible_values))
            
        return sorted(roll)
        
    def play_turn(self, player):
        """
        Player @param player plays until (1) they decide to pass or (2) they roll
        a non-scoring roll
        
        In this version of the game, each player always start with 6 available dice
        and 0 accrued pts
        
        Returns how many points the player got.
        Does NOT update game state
        """
        
        # in the simple version, each player starts with 0 pts and 6 dice
        self.num_available_dice = 6
        self.accrued_score = 0
        
        # update player game state
        player.update_game_state(self.pack_game_state())
        
        # player keeps rolling until they pass or bust
        keep_rolling = True
        busted = False
        
        while(keep_rolling):
            keep_rolling = player.pass_or_roll()
            
            if keep_rolling: # player wants to roll
            
                # roll the dice
                roll = self.roll_dice(self.num_available_dice)
                player.current_roll = roll
                
                # player makes choice on the dice
                choice = player.choose_dice()
                
                if choice == []:
                    busted = True
                    keep_rolling = False
                
                # process the player's choice. 
                # Update accrued pts, num_available_dice
                player.accrued_score += game_utils.get_score(choice)
                player.num_available_dice = player.num_available_dice - len(choice)
                if player.num_available_dice == 0:
                    player.num_available_dice = 6
        
        
        # after the player has decided to stop playing, (or has busted), return
        # their score
        if busted:
            return 0
        
        else:
            return player.accrued_score
            
        
        
        
    def play_game(self):
        """
        Players play turns interatively until one has 

        """
        current_player = 0 # start with first player
        keep_playing = True
        
        
        while (keep_playing):
            
            # the current player plays their turn
            score = self.play_turn(self.players(current_player))
            
            # updates game state after running the turn
            self.scores[current_player] += score
            
            # check to see if a player has won
            if self.scores[current_player] > WIN_THRESHOLD:
                keep_playing = False
                
            else:
                current_player += 1
                if current_player == len(self.players):
                    current_player = 0
                    
                    
        
        # TODO: report results/winner
        
        
        
        
        

