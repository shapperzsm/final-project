import sqlalchemy as sa
dbms = sa.create_engine('sqlite:///source-code/Database-code/Eperiment_Database.db')
connect_dbms_to_db = dbms.connect()


create_table = """
CREATE TABLE folk_theorem_experiment (
    experiment_number           INTEGER NOT NULL,
    player_strategy_name        TEXT NOT NULL,
    long_run_time_strategy      BOOLEAN NOT NULL,
    stochastic_strategy         BOOLEAN NOT NULL,
    memory_depth_of_strategy    INTEGER NOT NULL,
    prob_of_game_ending         REAL NOT NULL,
    payoff_matrix               TEXT NOT NULL,
    num_of_repetitions          INTEGER NOT NULL,
    nash_equilibria             TEXT NOT NULL,
    least_prob_of_defection     REAL NOT NULL,
    greatest_prob_of_defection  REAL NOT NULL,
    amount_of_noise             REAL NOT NULL,
        
    CONSTRAINT folk_theorem_experiment_pk PRIMARY KEY (experiment_number, player_strategy_name),
    CONSTRAINT prob_of_game_ending_ck CHECK (prob_of_game_ending BETWEEN 0 AND 1),
    CONSTRAINT least_prob_of_defection_ck CHECK (least_prob_of_defection BETWEEN 0 AND 1)
    CONSTRAINT greatest_prob_of_defection_ck CHECK (greatest_prob_of_defection BETWEEN 0 AND 1)
    CONSTRAINT amount_of_noise_ck CHECK (amount_of_noise BETWEEN 0 AND 1)
)
"""
connect_dbms_to_db.execute(create_table)