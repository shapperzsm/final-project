# import numpy as np
# import nashpy as nash
# import axelrod as axl
# import random
import functions

# import sqlalchemy as sa
# dbms = sa.create_engine('sqlite:///Experiment_Database.db')
# connect_dbms_to_db = dbms.connect()


players = functions.who_is_playing(3)
# players[0].name
# players[0].classifier['stochastic']
# players[0].classifier['memory_depth']
# players[0].classifier['long_run_time']
# players


# read_into_sql = """
# INSERT into folk_theorem_experiment
# (experiment_number, player_strategy_name, is_long_run_time, is_stochastic, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, num_of_equilibria, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, noise, could_be_degenerate)
#  VALUES
#  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
# """


trial_run = functions.get_game(
    tournament_repeat=30,
    player_list=players,
    prob_of_game_ending=0.22,
    set_seed=123,
    noise=0,
)
# matrix = trial_run['payoff matrix obtained']
defect = functions.get_prob_of_defection(
    trial_run["payoff matrix obtained"], "Support Enumeration"
)
# defect


for player in players:
    functions.write_record(
        experiment_number=1,
        player_strategy_name=player,
        is_long_run_time=player.classifier["long_run_time"],
        is_stochastic=player.classifier["stochastic"],
        memory_depth_of_strategy=player.classifier["memory_depth"],
        prob_of_game_ending=trial_run["probability of game ending"],
        payoff_matrix=trial_run["payoff matrix obtained"],
        num_of_repetitions=trial_run["number of tournament repeats"],
        nash_equilibria=defect["nash equilibria"],
        least_prob_of_defection=defect["least prob of defect"],
        greatest_prob_of_defection=defect["greatest prob of defect"],
        noise=trial_run["noise"],
        could_be_degenerate=False,
    )
