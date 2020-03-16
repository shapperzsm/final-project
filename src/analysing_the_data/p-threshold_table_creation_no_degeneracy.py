from pathlib import Path
import sqlalchemy as sa
import pandas as pd
import csv
import numpy as np

database_management_sys = sa.create_engine("sqlite:///../database_code/data/se/main.db")
connect_dbms_to_db = database_management_sys.connect()
data = pd.read_sql("folk_theorem_experiment", connect_dbms_to_db)


table_headings = pd.read_sql(
    "folk_theorem_experiment", connect_dbms_to_db
).columns.tolist()


p = Path("../database-code/data/prob_end_threshold")
p.mkdir(parents=True, exist_ok=True)

threshold_file = p / "main_no_degeneracy.csv"
with open(str(threshold_file), "w") as thresh_file:
    write_to_csv = csv.writer(thresh_file)
    write_to_csv.writerow(
        (
            "number_of_players",
            "tournament_player_set",
            "noise",
            "min_p_threshold",
            "mean_p_threshold",
            "median_p_threshold",
            "max_p_threshold",
        )
    )

max_tournament_player_set = """
    SELECT MAX(tournament_player_set) FROM folk_theorem_experiment
"""
max_num_of_player_sets = pd.read_sql(max_tournament_player_set, connect_dbms_to_db)
maximum_player_set = max_num_of_player_sets["MAX(tournament_player_set)"][0]
maximum_player_set

player_set_collection = """
    SELECT * FROM folk_theorem_experiment
    WHERE tournament_player_set = ?
    AND noise = ?
    AND player_strategy_name = 'Defector'
    AND warning_message = 'None'
"""

for each_set in range(maximum_player_set):
    for noise_level in np.linspace(0, 1, 11):
        collect_relevant_data = connect_dbms_to_db.execute(
            player_set_collection, each_set, noise_level
        )
        each_set_data = pd.DataFrame(
            collect_relevant_data.fetchall(), columns=table_headings
        )

        if noise_level in each_set_data["noise"]:
            num_of_players = each_set_data["number_of_players"].drop_duplicates()[0]

            indices_of_non_zero_defection_prob = each_set_data.index[
                each_set_data["least_prob_of_defection"] > 0
            ]

            if len(indices_of_non_zero_defection_prob) == 0:
                min_threshold = np.nan
                max_threshold = np.nan
                mean_threshold = np.nan
                median_threshold = np.nan

            elif len(indices_of_non_zero_defection_prob) == len(each_set_data):
                min_threshold = min(each_set_data["prob_of_game_ending"])
                max_threshold = min(each_set_data["prob_of_game_ending"])
                mean_threshold = min(each_set_data["prob_of_game_ending"])
                median_threshold = min(each_set_data["prob_of_game_ending"])

            else:
                jump_up_ending_probs = []
                for index in indices_of_non_zero_defection_prob:
                    if each_set_data.iloc[index - 1]["least_prob_of_defection"] == 0:
                        jump_up_ending_probs.append(
                            each_set_data.iloc[index]["prob_of_game_ending"]
                        )
                    else:
                        continue
                min_threshold = min(jump_up_ending_probs)
                max_threshold = max(jump_up_ending_probs)
                mean_threshold = np.mean(jump_up_ending_probs)
                median_threshold = np.median(jump_up_ending_probs)

            with open(str(threshold_file), "a") as thresh_file:
                write_to_csv = csv.writer(thresh_file)
                write_to_csv.writerow(
                    (
                        str(num_of_players),
                        str(each_set),
                        str(round(noise_level, 1)),
                        str(min_threshold),
                        str(mean_threshold),
                        str(median_threshold),
                        str(max_threshold),
                    )
                )
