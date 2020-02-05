from pathlib import *
import sqlalchemy as sa
import pandas as pd
import csv

database_management_sys = sa.create_engine("sqlite:///../database-code/data/se/main.db")
connect_dbms_to_db = database_management_sys.connect()
data = pd.read_sql("folk_theorem_experiment", connect_dbms_to_db)


table_headings = pd.read_sql(
    "folk_theorem_experiment", connect_dbms_to_db
).columns.tolist()


p = Path("../database-code/data/prob_end_threshold")
p.mkdir(parents=True, exist_ok=True)

threshold_file = p / "main-new.csv"
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
    AND player_strategy_name = 'Defector'
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
            if specific_noise_data["least_prob_of_defection"][0] >= 0.5:
                min_threshold = None
                mean_threshold = None
                median_threshold = None
                max_threshold = None
            else:
                min_threshold = 1
                mean_threshold = 1
                median_threshold = 1
                max_threshold = 1

        else:
            coop_is_better = specific_noise_data[
                specific_noise_data["least_prob_of_defection"] < 0.5
            ]
            defect_is_better = specific_noise_data[
                specific_noise_data["least_prob_of_defection"] >= 0.5
            ]
            if len(coop_is_better) == 0:
                max_threshold = None
                min_threshold = None
            elif len(defect_is_better) == 0:
                max_threshold = 1
                min_threshold = 1
            else:
                potential_max_threshold = max(coop_is_better["prob_of_game_ending"])
                if (
                    max(defect_is_better["prob_of_game_ending"])
                    <= potential_max_threshold
                ):
                    coop_is_better_less_than_defect = coop_is_better[
                        coop_is_better["least_prob_of_defection"]
                        < max(defect_is_better["least_prob_of_defection"])
                    ]
                    max_threshold = max(
                        coop_is_better_less_than_defect["prob_of_game_ending"]
                    )
                else:
                    max_threshold = max(coop_is_better["prob_of_game_ending"])

                min_threshold_for_defection = min(
                    defect_is_better["prob_of_game_ending"]
                )
                if min_threshold_for_defection == min(
                    specific_noise_data["prob_of_game_ending"]
                ):
                    min_threshold = None
                    max_threshold = None
                else:
                    min_threshold = max(
                        coop_is_better[
                            coop_is_better["prob_of_game_ending"]
                            < min_threshold_for_defection
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
                mean_threshold = threshold_between["prob_of_game_ending"].mean()
                median_threshold = threshold_between["prob_of_game_ending"].median()

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
