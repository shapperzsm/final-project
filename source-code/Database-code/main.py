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


read_into_sql = """
INSERT into folk_theorem_experiment 
    (experiment_number, player_strategy_name, long_run_time_strategy, stochastic_strategy, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, amount_of_noise)
VALUES 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


from collections import namedtuple
result = namedtuple('result', 'experiment_number, player_strategy_name, long_run_time_strategy, stochastic_strategy, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, amount_of_noise')


import numpy as np

def array_to_string(numpy_array):

    """
    A function which converts a numpy array into a space separated string.
    """

    flattened_array = numpy_array.flatten()
    flattened_array_to_string = str(flattened_array).strip('[]')
    return flattened_array_to_string




def string_to_array(string_of_int, num_of_rows, num_of_cols):

    """
    Numpy is required for this function to execute!

    A function which converts a string into a numpy array of the required dimensions, where:

    'string_of_int' is a space separated string variable containing integers;

    'num_of_rows' is an integer-valued variable stating the number of rows required for the array; and

    'num_of_cols' is an integer-valued variable stating the number of columns required for the array.
    """

    string_to_array = np.array([int(i) for i in string_of_int.split(' ')])
    reshape_array = np.reshape(string_to_array, (num_of_rows, num_of_cols))
    return reshape_array



payoff_matrix = np.array([[3, 0], [5, 1]])
payoff_matrix_as_string = array_to_string(payoff_matrix)

equilibria = [[1, 0, 0, 1], [0.3, 0.7, 0.7, 0.3]]
equilibria_as_string = str(str(equilibria).strip('[]').split('], [')).strip('[]')

record = result(1, 'Tit for Tat', False, False, 1, 0.4, payoff_matrix_as_string, 4, equilibria_as_string, 0, 0.944, 0)  

values = (record.experiment_number, record.player_strategy_name, record.long_run_time_strategy, record.stochastic_strategy, record.memory_depth_of_strategy, record.prob_of_game_ending, record.payoff_matrix, record.num_of_repetitions, record.nash_equilibria, record.least_prob_of_defection, record.greatest_prob_of_defection, record.amount_of_noise)
connect_dbms_to_db.execute(read_into_sql, values)