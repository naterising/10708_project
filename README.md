# 10708_project

Import the dice states:
  df = pd.read_parquet('data/dice_states_condensed.parquet')

## Project structure
+ data/
  + folder containing transition probabilities, reward tables, etc.
+ util.py
  + contains helper functions ie. generate choices, score function, etc.
+ mdp_greed.py
  + contains MDP logic that runs value iteration and outputs optimal policy
+ simulations/
  + contains scripts to enable simulating a game
  + paramaterize 1 or more players that inherit the Player class
  + run greed_sim.py to run a simulation
+ GAIL/
  + models trained by running train_imitator_dec_1.ipynb
  + checkpoint models and losses saved in dec1_imitator_1950.pth, dec1_discriminator_1950.pth, dec1_losses_1950.pkl
    

## Example usage
`python mdp.py`

to specify gamma and epsilon do

`python mdp.py <gamma> <epsilon>`


