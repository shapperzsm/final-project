from pathlib import *
import sqlalchemy as sa
import pandas as pd
import csv

database_management_sys = sa.create_engine("sqlite:///../database-code/data/se/main.db")
connect_dbms_to_db = database_management_sys.connect()
data = pd.read_sql("folk_theorem_experiment", connect_dbms_to_db)
len(data)


table_headings = pd.read_sql(
    "folk_theorem_experiment", connect_dbms_to_db
).columns.tolist()
table_headings


p = Path("../database-code/data/prob_end_threshold")
p.mkdir(parents=True, exist_ok=True)

threshold_file = p / "main.csv"
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
"""


for each_set in range(maximum_player_set):

    collect_relevant_data = connect_dbms_to_db.execute(player_set_collection, each_set)
    each_set_data = pd.DataFrame(
        collect_relevant_data.fetchall(), columns=table_headings
    )

    num_of_players = each_set_data["number_of_players"][0]

    for noise in list(each_set_data["noise"].drop_duplicates()):

        specific_noise_data = each_set_data[each_set_data["noise"] == noise]
        specific_noise_data.index = range(len(specific_noise_data))

        if len(specific_noise_data["least_prob_of_defection"]) == len(
            specific_noise_data[
                specific_noise_data["least_prob_of_defection"]
                == specific_noise_data["least_prob_of_defection"][0]
            ]
        ):
            if specific_noise_data["least_prob_of_defection"][0] == 1:
                min_threshold = min(specific_noise_data["prob_of_game_ending"])
                mean_threshold = min_threshold
                median_threshold = min_threshold
                max_threshold = min_threshold
            else:
                min_threshold = max(specific_noise_data["prob_of_game_ending"])
                mean_threshold = min_threshold
                median_threshold = min_threshold
                max_threshold = min_threshold

        else:
            zero_prob = specific_noise_data[
                specific_noise_data["least_prob_of_defection"] == 0
            ]
            non_zero_prob = specific_noise_data[
                specific_noise_data["least_prob_of_defection"] != 0
            ]

            if len(zero_prob) == 0:
                max_threshold = max(
                    specific_noise_data[
                        specific_noise_data["least_prob_of_defection"] != 1
                    ]["prob_of_game_ending"]
                )
            else:
                max_threshold = max(zero_prob["prob_of_game_ending"])

            min_threshold_non_zero = min(non_zero_prob["prob_of_game_ending"])
            if min_threshold_non_zero == min(
                specific_noise_data["prob_of_game_ending"]
            ):
                min_threshold = min_threshold_non_zero
            else:
                min_threshold = max(
                    zero_prob[
                        zero_prob["prob_of_game_ending"] < min_threshold_non_zero
                    ]["prob_of_game_ending"]
                )

            if min_threshold == max_threshold:
                mean_threshold = min_threshold
                median_threshold = min_threshold

            else:
                threshold_between = specific_noise_data[
                    (specific_noise_data["prob_of_game_ending"] >= min_threshold)
                    & (specific_noise_data["prob_of_game_ending"] <= max_threshold)
                ]

                threshold_between_not_zero = threshold_between[
                    threshold_between["least_prob_of_defection"] != 0
                ]

                if len(threshold_between_not_zero) == 0:
                    mean_threshold = threshold_between["prob_of_game_ending"].mean()
                    median_threshold = threshold_between["prob_of_game_ending"].median()
                else:
                    mean_threshold = threshold_between_not_zero[
                        "prob_of_game_ending"
                    ].mean()
                    median_threshold = threshold_between_not_zero[
                        "prob_of_game_ending"
                    ].median()

        with open(str(threshold_file), "a") as thresh_file:
            write_to_csv = csv.writer(thresh_file)
            write_to_csv.writerow(
                (
                    str(num_of_players),
                    str(each_set),
                    str(round(noise, 1)),
                    str(min_threshold),
                    str(mean_threshold),
                    str(median_threshold),
                    str(max_threshold),
                )
            )
