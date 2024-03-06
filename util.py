# -*- coding: utf-8 -*-
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)

def generate_states():
    """
    Generates all possible states

    Output: set of all possible states ie. {(6, ()), (3, (1, 4, 5)), (0, ())...}


    """

    logging.info('Generating states...')
    states = {(0, tuple([]))}

    # add keep states where you decide to roll or pass
    for i in range(1,7):
        states.add((i, tuple([])))

    # add roll states where you decide to score or you have to farkle
    ## N = 1
    for i in range(1,7):
        states.add((1, tuple([i])))

    ## N = 2
    [states.add((2, (i, j))) for i in range(1, 7) for j in range(1, 7)]

    ## N = 3
    [states.add((3, (i, j, k))) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7)]

    ## N = 4
    [states.add((4, (i, j, k, l))) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7) for l in range(1, 7)]

    ## N = 5
    [states.add((5, (i, j, k, l, m))) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7) for l in range(1, 7) for m
     in
     range(1, 7)]

    ## N = 6
    [states.add((6, (i, j, k, l, m, n))) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7) for l in range(1, 7) for
     m in
     range(1, 7) for n in range(1, 7)]

    return states


def score(choice):
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


def generate_choices():
    """
    Generates all possible scoring dice and their corresponding counts for each possible value a die can have

    Output: dictionary mapping scoring dice to their counts ie. {(1, 1): (1,0,0,0,0,0), (1, 1, 5, 5): (2,0,0,0,2,0)...}
    the counts are a vector where each entry is how many times its index appeared in the roll

    """

    logging.info('Generating choices...')
    roll_dict = {tuple([1]): np.array([1, 0, 0, 0, 0, 0]), tuple([5]): np.array([0, 0, 0, 0, 1, 0])}

    rolls = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    for roll in rolls:
        roll = tuple(sorted(roll))
        if score(roll):
            counts = np.zeros(6)
            for i in range(6):
                counts[i] = np.count_nonzero([i+1 == x for x in roll])
            roll_dict[roll] = counts
    ############################################

    rolls = [(i, j, k) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7)]

    for roll in rolls:
        roll = tuple(sorted(roll))
        if score(roll):
            counts = np.zeros(6)
            for i in range(6):
                counts[i] = np.count_nonzero([i+1 == x for x in roll])
            roll_dict[roll] = counts

    ############################################

    rolls = [(i, j, k, l) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7) for l in range(1, 7)]

    for roll in rolls:
        roll = tuple(sorted(roll))
        if score(roll):
            counts = np.zeros(6)
            for i in range(6):
                counts[i] = np.count_nonzero([i+1 == x for x in roll])
            roll_dict[roll] = counts

    ############################################

    rolls = [(i, j, k, l, m) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7) for l in range(1, 7) for m
             in
             range(1, 7)]

    for roll in rolls:
        roll = tuple(sorted(roll))
        if score(roll):
            counts = np.zeros(6)
            for i in range(6):
                counts[i] = np.count_nonzero([i+1 == x for x in roll])
            roll_dict[roll] = counts

    ############################################

    rolls = [(i, j, k, l, m, n) for i in range(1, 7) for j in range(1, 7) for k in range(1, 7) for l in range(1, 7) for
             m in
             range(1, 7) for n in range(1, 7)]

    for roll in rolls:
        roll = tuple(sorted(roll))
        if score(roll):
            counts = np.zeros(6)
            for i in range(6):
                counts[i] = np.count_nonzero([i+1 == x for x in roll])
            roll_dict[roll] = counts
    return roll_dict


POSSIBLE_CHOICES_COUNTS = generate_choices()

def scoring_choice_generator(roll):
    """
    Calculates possible scoring choices for a roll

    Input: list of numbers representing the roll
        - cannot be of length 0
        - cannot be of length greater than 6
        - each member of the list must be in {1,2,3,4,5,6}

    Output: list of scoring choices. if no valid choices then return a list containing empty list (the only option is a farkle)


    """

    allowed_entries = {1, 2, 3, 4, 5, 6}
    assert all(element in allowed_entries for element in roll)

    # sort the list
    roll = sorted(roll)

    # count occurrence of 1-6
    roll_counts = np.zeros(6)
    for i in range(6):
        roll_counts[i] = np.count_nonzero([i+1 == x for x in roll])
    choices = []
    # logging.debug(f"roll counts: {roll_counts}")
    for choice, counts in POSSIBLE_CHOICES_COUNTS.items():
        # logging.debug(f"choice: {choice}, counts: {counts}")
        if np.all((roll_counts - counts) >= 0):
            choices.append(choice)

    if len(choices) == 0: # farkle
        choices.append(tuple([]))
    return choices
