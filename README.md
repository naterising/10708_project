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

## Example usage
`python mdp.py`

to specify gamma and epsilon do

`python mdp.py <gamma> <epsilon>`


