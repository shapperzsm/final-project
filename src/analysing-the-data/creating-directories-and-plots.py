from pathlib import *
import sqlalchemy as sa
import pandas as pd
import os
import matplotlib.pyplot as plt
plt.rcParams.update({'figure.max_open_warning': 0})

database_management_sys = sa.create_engine('sqlite:///../../../../Desktop/rerun-data-no-long-run/se/main.db')
connect_dbms_to_db = database_management_sys.connect()

sql_no_degenerate = """
    SELECT * FROM folk_theorem_experiment
    WHERE warning_message = 'None'
"""

supp_en_data = pd.read_sql(sql_no_degenerate, connect_dbms_to_db)
# supp_en_data.head()

# len(supp_en_data)

grouped_supp_en = supp_en_data.groupby(["experiment_number"]).mean()
grouped_supp_en.head()

for num_of_players in grouped_supp_en["number_of_players"].drop_duplicates():
    
    p = Path("../../images/folk_thm/single_game/" + str(num_of_players) + "/")
    if p.exists() == False:
        p.mkdir(parents=True)
        print(str(p) + " was created.")
    else:
        print(str(p) + " already exists.")
    
    number_of_players_grouped_data = grouped_supp_en[grouped_supp_en["number_of_players"] == num_of_players]

    for player_set in number_of_players_grouped_data["tournament_player_set"].drop_duplicates():
        
        q = p / str(player_set)
        if q.exists() == False:
            q.mkdir()
            print(str(q) + " was created.")
        else:
            print(str(q) + " already exists.")

        player_set_grouped_data = number_of_players_grouped_data[number_of_players_grouped_data["tournament_player_set"] == player_set]

        for noise in player_set_grouped_data["noise"].drop_duplicates():
            noise = round(noise, 1)
            r = q / str(noise) 
            if r.exists() == False:
                r.mkdir()
                print(str(r) + " was created.")
            else:
                print(str(r) + " already exists.")

            noise_grouped_data = player_set_grouped_data[player_set_grouped_data["noise"] == noise]
            data_to_access_strategies = supp_en_data[(supp_en_data["number_of_players"] == num_of_players) & (supp_en_data["tournament_player_set"] == player_set) & (supp_en_data["noise"] == noise)]          
             
            markdown_path = r / "README.md"
            README = open(str(markdown_path), "w")
            README.write("# Single Game Plot \n" + " ## List of Players: \n" + str(data_to_access_strategies["player_strategy_name"].drop_duplicates()) + "\n ## Noise = " + str(noise))
            README.close()

            plot_path = r / "main.pdf"
            graph = plt.figure()
            axes = graph.add_subplot(1, 1, 1)
            axes.set_xlabel("$p =$ the probability of the game ending" )
            axes.set_ylabel("probability of defection in equilibria")
            axes.plot(noise_grouped_data["prob_of_game_ending"], noise_grouped_data["least_prob_of_defection"], "r", label = "least prob of defection")
            axes.plot(noise_grouped_data["prob_of_game_ending"], noise_grouped_data["greatest_prob_of_defection"], "y--", label = "greatest prob of defection")
            axes.legend()
            graph.savefig(str(plot_path))