import experiment_functions as expfun
import numpy as np


noise_probabilities = np.linspace(0, 1, 11)
game_ending_probabilities = np.linspace(0.001, 1 - 0.001, 100)

expfun.create_directory()
expfun.create_database("data/ve/")
print("Created table 'folk_theorem_experiment' in data/ve/main.db")
while True:
    expfun.run_experiment(
        max_num_of_opponents=9,
        number_of_player_samples=50,
        noise_probs=noise_probabilities,
        game_ending_probs=game_ending_probabilities,
        tournament_rep=100,
        database_filepath="data/ve/",
        support_enumeration=False,
    )
