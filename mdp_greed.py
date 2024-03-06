import csv
import itertools
import logging
import sys
import pandas
from util import score, scoring_choice_generator, generate_states

# init logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter( '%(levelname)s:%(module)s:%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

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
    Transitions = pandas.read_parquet(transitions_filepath)

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
        self.states = generate_states()
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
        return isinstance(action, (list, tuple)) and len(action) > 0

    def is_roll_action(self, action):
        """Returns True if the action is roll"""
        return isinstance(action, str) and action == 'roll'

    def is_pass_action(self, action):
        """Returns True if the action is pass"""
        return isinstance(action, str) and action == 'pass'

    def is_farkle(self, action):
        """Returns True if the action is a farkle ie. an empty set"""
        return isinstance(action, (list, tuple)) and len(action) == 0

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
            return scoring_choice_generator(state[1]) # returns list containing empty list if farkle
        if self.is_keep_state(state):
            if state[0] == 0: # used up all dice
                return {'pass'}
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
        if self.is_rolled_state(state):
            if self.is_score_action(action):
                return [(1, (state[0] - len(action),tuple([])))]
            if self.is_farkle(action):
                return [(1, (6, tuple([])))]
        if self.is_keep_state(state):
            if self.is_roll_action(action):
                tp = self.transition[self.transition.N == state[0]] # find all possible rolls of length N
                next_states = list(zip(tp.N, tp.roll.apply(tuple)))
                return list(zip(tp.p, next_states)) # return each possible roll of N dice and their probability of occurring
            if self.is_pass_action(action):
                return [(1, (6, tuple([])))]


def value_iteration(mdp, log_iters = 5):
    """
    Solving the MDP by value iteration.
    returns utility values for states after convergence

    Input: markov decision process model, number of iterations to log progress
    Output: optimized value function

    """
    states = mdp.states
    actions = mdp.actions
    T = mdp.T
    R = mdp.R

    # initialize value of all the states to 0 (this is k=0 case)
    V1 = {s: 0 for s in states}
    logger.info("Init values...")
    cnt = 0
    while True:
        V = V1.copy()
        delta = 0
        for s in states:
            # Bellman update, update the utility values
            logger.debug(f's = {s}')
            for a in actions(s):
                logger.debug(f"\t\ta = {a} T(s,a) = {T(s,a)}")
                logger.debug(f"\t\tr = {R(s,a)}")
            V1[s] = max([sum([p * (R(s, a) + gamma * V[s1]) for (p, s1) in T(s, a)]) for a in actions(s)])
            # calculate maximum difference in value
            delta = max(delta, abs(V1[s] - V[s]))

        cnt += 1
        if cnt % log_iters == 0:
            logger.info(f'completed {cnt} iterations. delta = {delta}')
        # check for convergence, if values converged then return V
        if delta < epsilon * (1 - gamma) / gamma:
            return V


def best_policy(mdp, V):
    """
    Given an MDP and a utility values V, determine the best policy as a mapping from state to action.
    returns policies which is dictionary of the form {state1: action1, state2: action2}

    Input: markov decision process model, optimized value function
    Output: the policy which maps each state to the best action

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


Transitions, Reward = read_file('data/dice_states_condensed.parquet', 'data/rewards.csv') # reward is a dummy variable left over from previous code
# Initialize the MarkovDecisionProcess object
mdp = MarkovDecisionProcess(transition=Transitions, reward=Reward)

# call value iteration
V = value_iteration(mdp)
for s in V:
    print(s, ' - ', V[s])
pi = best_policy(mdp, V)
logger.info("Finished value iteration. Saving policy...")
with open('data/policy.txt', 'w') as f:
    for s in pi:
        f.write(f"{s} - {pi[s]}\n")
