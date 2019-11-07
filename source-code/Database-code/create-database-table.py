import sqlalchemy as sa


def create_database(filepath):

    """
    A function which creates a database file, and an appropriate table, where the data collected from the
    experiments can be stored:

    'filepath' is a string containing the relative path to the place in where
    the file should be stored. The database file will be titled 'main.db'.
    """

    database_management_sys = sa.create_engine("sqlite:///" + filepath + "main.db")
    connect_dbms_to_db = database_management_sys.connect()

    create_table = """
    CREATE TABLE folk_theorem_experiment (
        experiment_number           INTEGER NOT NULL,
        player_strategy_name        TEXT NOT NULL,
        is_long_run_time            BOOLEAN NOT NULL,
        is_stochastic               BOOLEAN NOT NULL,
        memory_depth_of_strategy    TEXT NOT NULL,
        prob_of_game_ending         REAL NOT NULL,
        payoff_matrix               TEXT NOT NULL,
        num_of_repetitions          INTEGER NOT NULL,
        num_of_equilibria           INTEGER NOT NULL,
        nash_equilibria             TEXT NOT NULL,
        least_prob_of_defection     REAL NOT NULL,
        greatest_prob_of_defection  REAL NOT NULL,
        noise                       REAL NOT NULL,
        could_be_degenerate         BOOLEAN NOT NULL,
        
        CONSTRAINT folk_theorem_experiment_pk PRIMARY KEY (experiment_number, player_strategy_name),
        CONSTRAINT prob_of_game_ending_ck CHECK (prob_of_game_ending BETWEEN 0 AND 1),
        CONSTRAINT least_prob_of_defection_ck CHECK (least_prob_of_defection BETWEEN 0 AND 1)
        CONSTRAINT greatest_prob_of_defection_ck CHECK (greatest_prob_of_defection BETWEEN 0 AND 1)
        CONSTRAINT noise_ck CHECK (noise BETWEEN 0 AND 1)
    )
    """
    connect_dbms_to_db.execute(create_table)
    return database_management_sys.connect()
