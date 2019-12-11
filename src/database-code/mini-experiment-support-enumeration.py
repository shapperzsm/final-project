import experiment_functions as expfun
import numpy as np

noise_probabilities = [0, 0.1, 0.2, 0.3, 0.4, 0.5]
game_ending_probabilities = np.linspace(0.001, 1 - 0.001, 100)

expfun.create_directory()
expfun.create_database("data/se/")
print("Created table 'folk_theorem_experiment' in data/se/main.db")
while True:
    expfun.run_experiment(
        max_num_of_opponents=4,
        number_of_player_samples=5,
        noise_probs=noise_probabilities,
        game_ending_probs=game_ending_probabilities,
        tournament_rep=100,
        database_filepath="data/se/",
        support_enumeration=True,
    )
