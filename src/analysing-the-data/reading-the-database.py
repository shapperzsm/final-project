import sqlalchemy as sa
import pandas as pd

database_management_sys = sa.create_engine(
    "sqlite:///C:/Users/sophi/Desktop/rerun-data-no-long-run/se/main.db"
)
connect_dbms_to_db = database_management_sys.connect()

max_tournament_player_set = """
    SELECT MAX(tournament_player_set) FROM folk_theorem_experiment
"""
max_num_of_player_sets = pd.read_sql(max_tournament_player_set, connect_dbms_to_db)
maximum_player_set = max_num_of_player_sets["MAX(tournament_player_set)"][0]
maximum_player_set