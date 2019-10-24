from collections import namedtuple
import numpy as np

import sqlalchemy as sa
dbms = sa.create_engine('sqlite:///source-code/Database-code/Experiment_Database.db')
connect_dbms_to_db = dbms.connect()





def array_to_string(numpy_array):

    """
    A function which converts a numpy array into a space separated string.
    """

    flattened_array = numpy_array.flatten()
    flattened_array_to_string = str(flattened_array).strip('[]')
    return flattened_array_to_string




def string_to_array(string_of_float, num_of_rows, num_of_cols):

    """

    A function which converts a string into a numpy array of the required dimensions, where:

    'string_of_float' is a space separated string variable containing float;

    'num_of_rows' is an integer-valued variable stating the number of rows required for the array; and

    'num_of_cols' is an integer-valued variable stating the number of columns required for the array.
    """

    string_to_array = np.array([float(i) for i in string_of_float.split(' ')])
    reshape_array = np.reshape(string_to_array, (num_of_rows, num_of_cols))
    return reshape_array



read_into_sql = """
    INSERT into folk_theorem_experiment 
        (experiment_number, player_strategy_name, long_run_time_strategy, stochastic_strategy, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, amount_of_noise)
    VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


Record = namedtuple('Record', 'experiment_number, player_strategy_name, long_run_time_strategy, stochastic_strategy, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, amount_of_noise')



def Record(exp_num, player_strat_name, long_run_strat, stoch_strat,
strat_mem_depth, game_end_prob, payoff_mat, num_of_rep, nash_eq, least_prob,
greatest_prob, noise):
    
    """
    A function which writes the information gained from one player in the experiment to a single record in an SQL database, where:
    
    'exp_num' is a numeric variable stating the unique experiment number for the tournament;

    'player_strat_name' is a string containing the name of the strategy executed during the tournament;
    
    'long_run_strat' is a Boolean variable which states whether the strategy has a long running time (obtained from the Axelrod library);
    
    'stoch_strat' is a Boolean variable which states whether the strategy is categorised as stochastic in the Axelrod library;
    
    'strat_mem_depth' is a numeric variable which states the amount of memory the strategy has (obtained from the Axelrod library);
    
    'game_end_prob' is a numeric variable between 0 and 1 indicating the probability of the game ending in the tournament;
    
    'payoff_mat' is a Numpy array containing the mean payoff values obtained from the tournament results;
    
    'num_of_rep' is a numeric variable stating the number of times this tournament was repeated;
    
    'nash_eq' is a 'list of lists' containing the Nash Equilibria computed from the payoff
    """


#payoff_matrix = np.array([[3, 0], [5, 1]])
#payoff_matrix_as_string = array_to_string(payoff_matrix)

equilibria = [[1, 0, 0, 1], [0.3, 0.7, 0.7, 0.3]]
equilibria_as_string = str(str(equilibria).strip('[]').split('], [')).strip('[]')

#record = result(1, 'Tit for Tat', False, False, 1, 0.4, payoff_matrix_as_string, 4, equilibria_as_string, 0, 0.944, 0)  

#values = (record.experiment_number, record.player_strategy_name, #record.long_run_time_strategy, record.stochastic_strategy, #record.memory_depth_of_strategy, record.prob_of_game_ending, #record.payoff_matrix, record.num_of_repetitions, record.nash_equilibria, #record.least_prob_of_defection, record.greatest_prob_of_defection, #record.amount_of_noise)
#connect_dbms_to_db.execute(read_into_sql, values)