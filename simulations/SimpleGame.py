# -*- coding: utf-8 -*-
"""
Implements a simplified game class for running a Greed simulation:
- points don't carry over from one player to another
- each player starts their turn with 6 die available to roll and 0 pts accrued
- first player to 10000 pts wins (other players don't get one final turn)

"""
import random
import numpy as np
import game_utils
import logging
import os


WIN_THRESHOLD = 10000
SCORE_HISTORY_LENGTH = 1000

class SimpleGame:
    
    
    def __init__(self, players, log_file_path, score_data_path):
        """
        Each game 
        
        At the start, a list of players is passed to the game.
        These players will play the game in the order they 
        appear in the list.

        """
        
        self.players = players
        self.scores = [0 for i in range(len(players))]
        self.current_roll = tuple([]) # initially no dice have been rolled
        self.num_available_dice = 6 # start condition for simple gamme
        self.accrued_score = 0 # start condition for simple game
        
        
        # initialize data structures that track scores over time
        self.full_score_history = np.zeros((SCORE_HISTORY_LENGTH,len(players))) 
        self.score_data_path = score_data_path
        
        # ensure clean logging configuration
        logging.shutdown()
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
            
            
        # setup log for game
        logging.basicConfig(filename=log_file_path, filemode ="w",format='%(message)s')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        
        

        
    def pack_game_state(self):
        return (self.scores, self.num_available_dice, self.accrued_score)
    
    def roll_dice(self, n):
        """
        Rolls n dice
        """
        possible_values = [1,2,3,4,5,6]
        
        roll = []
        for i in range(n):
            roll.append(random.choice(possible_values))
            
        return tuple(sorted(roll))
        
    def play_turn(self, player):
        """
        Player @param player plays until (1) they decide to pass or (2) they roll
        a non-scoring roll
        
        In this version of the game, each player always start with 6 available dice
        and 0 accrued pts
        
        Returns how many points the player got.
        Does NOT update game state
        """
        self.logger.info("Player " + str(player.player_num) + " taking a turn...")
        
        
        # in the simple version, each player starts with 0 pts and 6 dice
        player.num_available_dice = self.num_available_dice
        player.accrued_score = self.accrued_score
        
        # update player game state
        player.update_game_state(self.pack_game_state())
        
        # player keeps rolling until they pass or bust
        keep_rolling = True
        busted = False
        
        while(keep_rolling):
            self.logger.info("\tCurrent state: "+str(player.num_available_dice) + " dice available to roll, " + str(player.accrued_score) + " accrued points")
            keep_rolling = player.pass_or_roll()
            
            
            if keep_rolling: # player wants to roll
                self.logger.info("\tplayer wants to roll...")
            
                # roll the dice
                roll = self.roll_dice(player.num_available_dice)
                player.current_roll = roll
                self.logger.info("\t\troll: [%s]", ','.join(map(str, roll)))
                
                
                # player makes choice on the dice
                choice = player.choose_dice()
                self.logger.info("\t\tplayer choice: [%s]", ','.join(map(str, choice)))

                
                if choice == []:
                    busted = True
                    keep_rolling = False
                    self.logger.info("\t\t\tplayer busted! Turn over...")
                
                # process the player's choice. 
                # Update accrued pts, num_available_dice
                choice_score = game_utils.get_score(choice)
                self.logger.info("\t\t\tplayer accrued " + str(choice_score) + " points from choice..." )
                
                
                player.accrued_score += choice_score
                player.num_available_dice = player.num_available_dice - len(choice)
                if player.num_available_dice == 0:
                    player.num_available_dice = 6
                    
            else:
                self.logger.info("\tplayer wants to pass. Turn over...")
        
        
        # after the player has decided to stop playing, (or has busted), return
        # their score. 
        if busted:
            return 0
        
        else:
            return player.accrued_score
            
    def get_final_scores(self,all_scores):
        """
        Strip last row of scores array, and fill in any 0-values with value in 
        previous row. Called at end of play_game() function
        """
                
        num_rows = all_scores.shape[0]
        final_row = all_scores[-1]
                
        for i in range(len(final_row)):
            if final_row[i] == 0:
                final_row[i] = all_scores[num_rows-2,i]
            
        return final_row
        
        
    def play_game(self):
        """
        Players play turns interatively until one has 

        """
        
        self.logger.info("--------------------------------------------------")
        self.logger.info("Starting Game...")
        
        current_player = 0 # start with first player
        keep_playing = True
        round_num = 0
        
        
        while (keep_playing):
            
            # the current player plays their turn
            score = self.play_turn(self.players[current_player])
            
            # updates game state after running the turn
            self.scores[current_player] += score
            self.full_score_history[round_num,current_player] = self.scores[current_player]
            
            # check to see if a player has won
            if self.scores[current_player] > WIN_THRESHOLD:
                keep_playing = False
                
            else:
                current_player += 1
                if current_player == len(self.players):
                    current_player = 0
                    round_num += 1
                    
                    
        # save results
        final_scores = self.full_score_history[:round_num+1]
        headers = ["Player " + str(i) for i in range(len(self.players))]
        np.savetxt(self.score_data_path,final_scores,delimiter=',',header=','.join(map(str, headers)),comments="",fmt='%.{}f'.format(0))
    
        
        # return final scores
        return self.get_final_scores(final_scores)
    

        
        

        
        
        
        
        
        

