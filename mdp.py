import csv, itertools, logging, pickle, sys, os
import pandas
from multiprocessing import Pool
from utils import score, scoring_choice_generator, generate_states, generate_choices
import random, time

import numpy as np

N_PROC = os.cpu_count()

# init logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)s:%(module)s:%(message)s')
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

        self.choices = generate_choices()

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
        if self.is_keep_state(state):
            if self.is_pass_action(action):
                return -10000
            else:
                return 0
        elif self.is_rolled_state(state):
            if self.is_score_action(action):
                return score(action)
            elif self.is_farkle(action):
                return -10000
            else:
                raise Exception('Invalid action')
        else:
            raise Exception('Invalid state')

    def actions(self, state):
        """return set of actions that can be performed in this state"""
        """
        if state is (N, r), where n is number of dice and r is roll sequence, actions are score or farkle depending on roll sequence
        if state is (N, {}), actions are pass or roll
        """
        if self.is_rolled_state(state):
            return scoring_choice_generator(state[1], self.choices)  # returns list containing empty list if farkle
        if self.is_keep_state(state):
            if state[0] == 0:  # used up all dice
                return ['pass']
            return ['pass', 'roll']

    def T(self, state, action):
        """for a state and an action, return a list of (probability, result-state) pairs."""
        """
        if state is (N, r), where n is number of dice and r is roll sequence
        -- if action is score, next state is (N - k, {}), where k is number of chosen dice to score
        *special case, if k == N, then set N = 6
        -- if action is farkle, next state is (6, {})
        if state is (N, {})
        -- if action is roll, next state is set of (N, r) with precomputed probabilities
        -- if action is pass, next state is (6, {}) 
        """
        if self.is_rolled_state(state):  # state is (N, r)
            if self.is_score_action(action):
                if len(action) == 6: return [(1, (6, tuple([])))]
                return [(1, (state[0] - len(action), tuple([])))]
            if self.is_farkle(action):
                return [(1, (6, tuple([])))]
        if self.is_keep_state(state):  # state is (N, {})
            if self.is_roll_action(action):
                tp = self.transition[self.transition.N == state[0]]  # find all possible rolls of length N
                next_states = list(zip(tp.N, tp.roll.apply(tuple)))
                return list(
                    zip(tp.p, next_states))  # return each possible roll of N dice and their probability of occurring
            if self.is_pass_action(action):
                return [(1, (6, tuple([])))]

def Q_value(mdp, s, a, V, gamma = 0.9):
    return sum([p * (mdp.R(s, a) + gamma * V[s1]) for (p, s1) in mdp.T(s, a)])

def policy_evaluation(mdp, policy, V, epsilon=1e-4, gamma = 0.9, log_iters = 10):

        cnt = 0
        while True:
            delta = 0.0
            for state in mdp.states:
                # Calculate the value of V(s)
                old_value = V[state]
                new_value = Q_value(mdp, state, policy[state], V, gamma)
                V[state] = new_value
                delta = max(delta, abs(old_value - new_value))

            cnt += 1
            if cnt % log_iters == 0:
                logger.debug(f'iter {cnt} of policy evaluation, delta = {delta}')
            # terminate if the value function has converged
            if delta < epsilon:
                return V

def policy_iteration(mdp, epsilon = 1e-4, gamma = 0.9, log_iters = 10):
    """
    Solving the MDP by policy iteration.
    returns the policy after it converges

    Input: markov decision process, the number of iterations to log progress
    Output: optimized policy 
    """
    states = mdp.states
    actions = mdp.actions
    T = mdp.T
    R = mdp.R

    # init random policy
    policy = {s: random.choice(actions(s)) for s in states}
    V = {s: 0 for s in states}
    cnt = 0
    while True:
        V = policy_evaluation(mdp, policy, V, epsilon, gamma, log_iters = 50)
        policy_changed = False
        for s in states:
            old_action = policy[s]
            action_set = actions(s)
            policy[s] = action_set[np.argmax([Q_value(mdp, s, a, V, gamma) for a in action_set], keepdims=True)[0]]
            if old_action != policy[s]:
                policy_changed = True

        cnt += 1
        if cnt % log_iters == 0:
            logger.info(f'completed {cnt} iterations of policy iteration')

        if not policy_changed:
            return policy, V

def value_iteration(mdp, epsilon = 1e-4, gamma = 0.9, log_iters=10):
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
    V = {s: 0 for s in states}
    logger.info("Init values...")
    cnt = 0
    while True:
        delta = 0
        for s in states:
            old_value = V[s]
            V[s] = max([Q_value(s, a, V, gamma) for a in actions(s)])
            # calculate maximum difference in value
            delta = max(delta, abs(V[s] - old_value))

        cnt += 1
        if cnt % log_iters == 0:
            logger.info(f'completed {cnt} iterations of value iteration. delta = {delta}')
        # check for convergence, if values converged then return V
        if delta < epsilon:
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


if __name__ == '__main__':

    Transitions, Reward = read_file('data/dice_states_condensed.parquet',
                                    'data/rewards.csv')  # reward is a dummy variable left over from previous code
    # Initialize the MarkovDecisionProcess object
    mdp = MarkovDecisionProcess(transition=Transitions, reward=Reward)
    
    # call value iteration
    # V = value_iteration(mdp)
    # with open('data/policies/value gamma=0.9 penalty = -10000 farkle penalty.pkl', 'wb') as f:
    #     pickle.dump(V, f, pickle.HIGHEST_PROTOCOL)
    
    # with open('data/policies/value gamma=0.9 penalty = -10000 farkle penalty.txt', 'w') as f:  # TODO: rewrite in pandas parlance
    #     for s in V:
    #         f.write(f"{s} - {V[s]}\n")
    
    # pi = best_policy(mdp, V)
    # logger.info("Finished value iteration. Saving policy...")  # TODO: rewrite in pandas parlance
    # with open('data/policies/policy gamma=0.9 penalty = -10000 farkle penalty.txt', 'w') as f:
    #     for s in pi:
    #         f.write(f"{s} - {pi[s]}\n")
    
    # with open('data/policies/policy gamma=0.9 penalty = -10000 farkle penalty.pkl', 'wb') as f:
    #     pickle.dump(pi, f, pickle.HIGHEST_PROTOCOL)

    # call policy iteration
    start_t = time.time()
    P, V = policy_iteration(mdp, log_iters=10)
    end_t = time.time()

    logger.info(f"Finished Policy iteration. Time elapsed = {end_t - start_t}. Saving policy...")  # TODO: rewrite in pandas parlance

    with open('data/policies/policy iteration/value gamma=0.9 penalty = -10000 farkle penalty.pkl', 'wb') as f:
        pickle.dump(V, f, pickle.HIGHEST_PROTOCOL)
    
    with open('data/policies/policy iteration/value gamma=0.9 penalty = -10000 farkle penalty.txt', 'w') as f:  # TODO: rewrite in pandas parlance
        for s in V:
            f.write(f"{s} - {V[s]}\n")

    with open('data/policies/policy iteration/policy gamma=0.9 penalty = -10000 farkle penalty.txt', 'w') as f:
        for s in P:
            f.write(f"{s} - {P[s]}\n")
    
    with open('data/policies/policy iteration/policy gamma=0.9 penalty = -10000 farkle penalty.pkl', 'wb') as f:
        pickle.dump(P, f, pickle.HIGHEST_PROTOCOL)
