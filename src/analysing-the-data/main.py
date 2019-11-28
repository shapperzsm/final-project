from pathlib import *
import sqlalchemy as sa
import pandas as pd
import os
import matplotlib.pyplot as plt

plt.rcParams.update({"figure.max_open_warning": 0})

import random


database_management_sys = sa.create_engine(
    "sqlite:///../../../../Desktop/rerun-data-no-long-run/se/main.db"
)
connect_dbms_to_db = database_management_sys.connect()

table_headings = pd.read_sql(
    "folk_theorem_experiment", connect_dbms_to_db
).columns.tolist()
table_headings

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

# for num_of_sets in range(maximum_player_set):
for num_of_sets in [random.randint(0, maximum_player_set) for index in range(10)]:
    collect_relevant_data = connect_dbms_to_db.execute(
        player_set_collection, num_of_sets
    )
    num_of_set_data = pd.DataFrame(
        collect_relevant_data.fetchall(), columns=table_headings
    )

    num_of_players = num_of_set_data["number_of_players"][0]

    for noise in list(num_of_set_data["noise"].drop_duplicates()):

        p = Path(
            "../../images/folk_thm/single_game/"
            + str(num_of_players)
            + "/"
            + str(num_of_sets)
            + "/"
            + str(noise)
            + "/"
        )

        p.mkdir(parents=True, exist_ok=True)

        markdown_path = p / "README.md"
        strategy_table = pd.DataFrame(
            num_of_set_data[
                [
                    "player_strategy_name",
                    "is_long_run_time",
                    "is_stochastic",
                    "memory_depth_of_strategy",
                ]
            ].iloc[list(range(num_of_players))]
        )
        with open(str(markdown_path), "w") as README:
            README.write(
                "# Single Game Plot \n"
                + "Player Strategy Data:\n"
                + str(strategy_table)
                + "\n ## Noise = "
                + str(noise)
            )

        specific_noise_data = num_of_set_data[num_of_set_data["noise"] == noise]
        if specific_noise_data["warning_message"].all() == "None":
            plot_path = p / "main.pdf"
            graph = plt.figure()
            axes = graph.add_subplot(1, 1, 1)
            axes.set_xlabel("$p =$ the probability of the game ending")
            axes.set_ylabel("probability of defection in equilibria")
            axes.plot(
                specific_noise_data["prob_of_game_ending"],
                specific_noise_data["least_prob_of_defection"],
                "r",
                label="least prob of defection",
            )
            axes.plot(
                specific_noise_data["prob_of_game_ending"],
                specific_noise_data["greatest_prob_of_defection"],
                "y--",
                label="greatest prob of defection",
            )
            axes.legend()
            graph.savefig(str(plot_path))
            plt.close()
        else:
            plot_path = p / "main.pdf"
            graph = plt.figure()
            axes = graph.add_subplot(1, 1, 1)
            axes.set_xlabel("$p =$ the probability of the game ending")
            axes.set_ylabel("probability of defection in equilibria")
            degenerate_data = specific_noise_data[
                specific_noise_data["warning_message"] != "None"
            ]
            non_degen_data = specific_noise_data[
                specific_noise_data["warning_message"] == "None"
            ]
            colours = ["r", "y", "b", "g"]
            linestyles = ["-", "--", "-", "--"]
            data_list = [
                non_degen_data["least_prob_of_defection"],
                non_degen_data["greatest_prob_of_defection"],
                degenerate_data["least_prob_of_defection"],
                degenerate_data["greatest_prob_of_defection"],
            ]
            label_list = [
                "least prob of defection",
                "greatest prob of defection",
                "least prob of defection (could be degenerate)",
                "greatest prob of defection (could be degenerate)",
            ]
            game_ending_probabilities = [
                non_degen_data["prob_of_game_ending"],
                non_degen_data["prob_of_game_ending"],
                degenerate_data["prob_of_game_ending"],
                degenerate_data["prob_of_game_ending"],
            ]
            for xvalues, data, linestyle, colour, label in zip(
                game_ending_probabilities, data_list, linestyles, colours, label_list
            ):
                axes.plot(xvalues, data, linestyle=linestyle, color=colour, label=label)
            axes.legend()
            graph.savefig(str(plot_path))
            plt.close()

            degenerate_experiment_num = degenerate_data["experiment_number"]
            degenerate_game_ending_prob = degenerate_data["prob_of_game_ending"]
            degenerate_payoff_matrix = degenerate_data["payoff_matrix"]
            degenerate_details = pd.concat(
                [
                    degenerate_experiment_num,
                    degenerate_game_ending_prob,
                    degenerate_payoff_matrix,
                ],
                axis=1,
            ).drop_duplicates()
            degen_markdown_path = p / "degenerate.md"
            degenerate_info = open(str(degen_markdown_path), "w")
            degenerate_info.write(
                "# Potentially degenerate games were used in this plot.\n"
                + "## Details of specific games which could be degenerate.\n"
                + str(degenerate_details)
            )
            degenerate_info.close()
