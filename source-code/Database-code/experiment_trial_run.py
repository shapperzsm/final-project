import experiment_functions as expfun
import numpy as np

stochasticity = np.linspace(0, 1, 11)
prob_of_game_end = np.linspace(0.001, 1-0.001, 5)
experiment_number = 1

expfun.create_database("data/support_enumeration/")
for noise in stochasticity:

    expfun.run_experiment(max_num_of_opponents=4, tournament_repeats=10, game_ending_probs=prob_of_game_end, seed=123, noise=noise, database_filepath="data/support_enumeration/", num_of_opponents=1, experiment_num=experiment_number, support_enumeration=True)
    
    experiment_number += 20