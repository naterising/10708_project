# -*- coding: utf-8 -*-
"""
Utility functions to help with Greed simulation
"""

from itertools import combinations

def get_score(choice):
    """
    Calculates reward for some choice of dice to keep

    Input: list of numbers representing kept dice
        - cannot be of length 0
        - cannot be of length greater than 6
        - each member of the list must be in {1,2,3,4,5,6}

    Output: reward (in points) of choosing that combination


    """

    assert len(choice) > 0
    assert len(choice) < 7

    allowed_entries = set([1, 2, 3, 4, 5, 6])
    assert all(element in allowed_entries for element in choice)

    # sort the list
    choice = sorted(choice)

    if choice == [1]:
        return 100

    elif choice == [5]:
        return 50

    elif choice == [1, 5]:
        return 150

    elif choice == [1, 1]:
        return 200

    elif choice == [5, 5]:
        return 100

    elif choice == [1, 1, 1]:
        return 1000

    elif choice == [2, 2, 2]:
        return 200

    elif choice == [3, 3, 3]:
        return 300

    elif choice == [4, 4, 4]:
        return 400

    elif choice == [5, 5, 5]:
        return 500

    elif choice == [6, 6, 6]:
        return 600

    elif choice == [1, 1, 5]:
        return 250

    elif choice == [1, 5, 5]:
        return 200

    elif choice == [1, 1, 1, 1]:
        return 2000

    elif choice == [2, 2, 2, 2]:
        return 400

    elif choice == [3, 3, 3, 3]:
        return 600

    elif choice == [4, 4, 4, 4]:
        return 800

    elif choice == [5, 5, 5, 5]:
        return 1000

    elif choice == [6, 6, 6, 6]:
        return 1200

    elif choice == [1, 1, 1, 5]:
        return 1050  # 3x1 = 1000 + 50

    elif choice == [1, 1, 5, 5]:
        return 300

    elif choice == [1, 5, 5, 5]:
        return 600  # 3x5 = 500 + 100

    elif choice == [1, 1, 1, 1, 1]:
        return 4000

    elif choice == [2, 2, 2, 2, 2]:
        return 800

    elif choice == [3, 3, 3, 3, 3]:
        return 1200

    elif choice == [4, 4, 4, 4, 4]:
        return 1600

    elif choice == [5, 5, 5, 5, 5]:
        return 2000

    elif choice == [6, 6, 6, 6, 6]:
        return 2400

    elif choice == [1, 1, 1, 1, 5]:
        return 2050

    elif choice == [1, 1, 1, 5, 5]:
        return 1100

    elif choice == [1, 1, 5, 5, 5]:
        return 700

    elif choice == [1, 5, 5, 5, 5]:
        return 1100

    elif choice == [1, 1, 1, 1, 1, 1]:
        return 8000

    elif choice == [2, 2, 2, 2, 2, 2]:
        return 1600

    elif choice == [3, 3, 3, 3, 3, 3]:
        return 2400

    elif choice == [4, 4, 4, 4, 4, 4]:
        return 3200

    elif choice == [5, 5, 5, 5, 5, 5]:
        return 4000

    elif choice == [6, 6, 6, 6, 6, 6]:
        return 4800

    elif choice == [1, 1, 1, 1, 1, 5]:
        return 4050

    elif choice == [1, 1, 1, 1, 5, 5]:
        return 2100

    elif choice == [1, 1, 1, 5, 5, 5]:
        return 1500

    elif choice == [1, 1, 5, 5, 5, 5]:
        return 1200

    elif choice == [1, 5, 5, 5, 5, 5]:
        return 2100

    # if control reaches here the choice is either a bust or 3 pairs
    if len(choice) != 6: return 0

    # if control reaches here the choice is a len=6 list
    # determine if the (sorted) list has 3 pairs
    num_pairs = 0
    for i in range(5):
        if choice[i] == choice[i + 1] and i % 2 == 0:
            num_pairs += 1

    if num_pairs == 3:
        return 1000

    else:
        return 0
    
    
def get_possible_choices(roll):
    """
    Enumerates all possible choices that a player could pick on a given roll.
    Returns a list of tuples that define a roll choice
    """
    
    all_combinations = set()
    
    for i in range(1,len(roll)+1):
        # Get all possible combinations of length i
        all_combinations = all_combinations.union(set(combinations(roll, i)))

    return list(all_combinations)

def get_highest_choice(all_choices):
    """
    Given a list of every possible choice, returns a tuple (choice, score)
    that gives the highest possible score. If mutiple rolls give that score, 
    the one that uses the least amount of dice is used. 
    
    Returns [] if no scoring rolls are possible
    """
    
    highest_choice = []
    highest_score = 0
    
    for choice in all_choices:
        score = get_score(list(choice))
        
        if score > highest_score or (score == highest_score and len(choice) < len(highest_choice)):
            highest_score = score
            highest_choice = choice
            
    if highest_score > 0:
        best = list(highest_choice)
    
    else:
        best = []
        
    print(best)
    return best
        
    
            
        
