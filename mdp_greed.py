import csv
import itertools
import sys
from util import score, scoring_choice_generator

# gamma is the discount factor
if len(sys.argv) > 1:
    gamma = float(sys.argv[1])
else:
    gamma = 0.9

# the maximum error allowed in the utility of any state
if len(sys.argv) > 2:
    epsilon = float(sys.argv[2])
else:
    epsilon = 0.001


def read_file(transitions_filepath, rewards_filepath):
    Transitions = {}
    Reward = {}

    # read transitions from file and store it to a variable
    with open(transitions_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] in Transitions:
                if row[1] in Transitions[row[0]]:
                    Transitions[row[0]][row[1]].append((float(row[3]), row[2]))
                else:
                    Transitions[row[0]][row[1]] = [(float(row[3]), row[2])]
            else:
                Transitions[row[0]] = {row[1]: [(float(row[3]), row[2])]}

    # read rewards file and save it to a variable
    with open(rewards_filepath, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            Reward[row[0]] = float(row[1]) if row[1] != 'None' else None
    return Transitions, Reward


class MarkovDecisionProcess:
    """A Markov Decision Process, defined by an states, actions, transition model and reward function."""

    def __init__(self, transition={}, reward={}, gamma=.9):
        # collect all nodes from the transition models
        self.states = transition.keys()
        # initialize transition
        self.transition = transition
        # initialize reward
        self.reward = reward
        # initialize gamma
        self.gamma = gamma

    def is_rolled_state(self, state):
        """Returns True if the state is after getting a roll"""
        return len(state[1]) > 0
    def is_keep_state(self, state):
        """Returns True if the state is before deciding to roll or pass"""
        return len(state[1]) == 0

    def is_score_action(self, action):
        """Returns True if the action is a scoring action ie. a non-empty set"""
        return isinstance(action, set) and action

    def is_farkle(self, action):
        """Returns True if the action is a farkle ie. an empty set"""
        return isinstance(action, set) and not action

    def R(self, state, action):
        """return reward for this state."""
        """
        if state is (N, r), where n is number of dice and r is roll sequence
        -- if action is a score, return score(action)
        -- if only action is farkle (r had empty scoring set), return -accrued points #TODO dummy value for this
        if state is (N, {}) return 0
        """
        if self.is_keep_state(state): return 0
        elif self.is_rolled_state(state):
            if self.is_score_action(action): return score(action)
            elif self.is_farkle(action): return 0
            else: raise Exception('Invalid action')
        else: raise Exception('Invalid state')

    def actions(self, state):
        """return set of actions that can be performed in this state"""
        """
        if state is (N, r), where n is number of dice and r is roll sequence, actions are score or farkle depending on roll sequence
        if state is (N, {}), actions are pass or roll
        """
        if self.is_rolled_state(state):
            return scoring_choice_generator(state[1]) # if empty this is interpreted as a farkle
        if self.is_keep_state(state):
            return {'pass', 'roll'}


    def T(self, state, action):
        """for a state and an action, return a list of (probability, result-state) pairs."""
        """
        if state is (N, r), where n is number of dice and r is roll sequence
        -- if action is score, next state is (N - k, {}), where k is number of chosen dice to score
        -- if action is farkle, next state is (6, {})
        if state is (N, {})
        -- if action is roll, next state is set of (N, r) with precomputed probabilities
        -- if action is pass, next state is (6, {}) 
        """
        pass


def value_iteration(mdp):
    """
    Solving the MDP by value iteration.
    returns utility values for states after convergence
    """
    states = mdp.states
    actions = mdp.actions
    T = mdp.T
    R = mdp.R

    # initialize value of all the states to 0 (this is k=0 case)
    V1 = {s: 0 for s in states}
    while True:
        V = V1.copy()
        delta = 0
        for s in states:
            # Bellman update, update the utility values
            V1[s] = max([sum([p * (R(s, a) + gamma * V[s1]) for (p, s1) in T(s, a)]) for a in actions(s)])
            # calculate maximum difference in value
            delta = max(delta, abs(V1[s] - V[s]))

        # check for convergence, if values converged then return V
        if delta < epsilon * (1 - gamma) / gamma:
            return V


def best_policy(mdp, V):
    """
    Given an MDP and a utility values V, determine the best policy as a mapping from state to action.
    returns policies which is dictionary of the form {state1: action1, state2: action2}
    """
    states = mdp.states
    actions = mdp.actions
    pi = {}
    for s in states:
        pi[s] = max(actions(s), key=lambda a: expected_utility(mdp, a, s, V))
    return pi


def expected_utility(mdp, a, s, V):
    """returns the expected utility of doing a in state s, according to the MDP and V."""
    T = mdp.T
    return sum([p * V[s1] for (p, s1) in mdp.T(s, a)])


Transitions, Reward = read_file('data/transitions.csv', 'data/rewards.csv')
# Initialize the MarkovDecisionProcess object
mdp = MarkovDecisionProcess(transition=Transitions, reward=Reward)

# call value iteration
V = value_iteration(mdp)
print('State - Value')
for s in V:
    print(s, ' - ', V[s])
pi = best_policy(mdp, V)
print('\nOptimal policy is \nState - Action')
for s in pi:
    print(s, ' - ', pi[s])
