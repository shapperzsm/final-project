import functions
import numpy as np

stochasticity = np.linspace(0, 1, 11)
prob_of_game_end = np.linspace(0.001, 1-0.001, 5)

for noise in stochasticity:

    functions.run_experiment(max_num_of_opponents=4, tournament_repeats=10, game_ending_probs=prob_of_game_end, seed=123, equilibrium_algorithm="Support Enumeration", noise=noise, num_of_opponents=1)