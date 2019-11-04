import experiment_functions as expfun
import numpy as np

noise_probabilities = np.linspace(0, 1, 11)
game_ending_probabilities = np.linspace(0.001, 1-0.001, 5)

expfun.create_database("data/support_enumeration/")
expfun.run_experiment(max_num_of_opponents=4, number_of_player_samples=5, noise_probs=noise_probabilities, game_ending_probs=game_ending_probabilities, tournament_rep=10, database_filepath="data/support_enumeration/", support_enumeration=True)

expfun.create_database("data/vertex_enumeration/")
expfun.run_experiment(max_num_of_opponents=4, number_of_player_samples=5, noise_probs=noise_probabilities, game_ending_probs=game_ending_probabilities, tournament_rep=10, database_filepath="data/vertex_enumeration/", support_enumeration=False)