import numpy as np
import nashpy as nash
import axelrod as axl
import random
import warnings
import sqlalchemy as sa


################################################################################
def create_database(filepath):

    """
    A function which creates a database file, and an appropriate table, where the data collected from the
    experiments can be stored:

    'filepath' is a string containing the relative path to the place in where
    the file should be stored. The database file will be titled 'main.db'.
    """

    database_management_sys = sa.create_engine('sqlite:///' + filepath + 'main.db')
    connect_dbms_to_db = database_management_sys.connect()


    create_table = """
    CREATE TABLE IF NOT EXISTS folk_theorem_experiment (
        experiment_number           INTEGER NOT NULL,
        player_strategy_name        TEXT NOT NULL,
        is_long_run_time            BOOLEAN NOT NULL,
        is_stochastic               BOOLEAN NOT NULL,
        memory_depth_of_strategy    TEXT NOT NULL,
        prob_of_game_ending         REAL NOT NULL,
        payoff_matrix               TEXT NOT NULL,
        num_of_repetitions          INTEGER NOT NULL,
        num_of_equilibria           INTEGER,
        nash_equilibria             TEXT,
        least_prob_of_defection     REAL,
        greatest_prob_of_defection  REAL,
        noise                       REAL NOT NULL,
        warning_message             TEXT,
        
        CONSTRAINT folk_theorem_experiment_pk PRIMARY KEY (experiment_number, player_strategy_name)
    )
    """
    connect_dbms_to_db.execute(create_table)


################################################################################
def who_is_playing(num_of_opponents, long_run_strategies=False):
    """
    A function to choose which strategies will be playing against the Defector, where:

    'num_of_opponents' is a numeric variable which states how many players will 
    be competing (EXCLUDING the Defector); and

    'long_run_strategies' is a Boolean variable which states whether strategies 
    which have a long running time should be included in the competitors or 
    not. It has a default value of False.

    A list containing the selected strategies is returned.
    """

    if long_run_strategies == True:
        filterstrategies = {
            "manipulates_state": False,
            "manipulates_source": False,
            "inspects_source": False,
        }
    else:
        filterstrategies = {
            "long_run_time": False,
            "manipulates_state": False,
            "manipulates_source": False,
            "inspects_source": False,
        }

    filtered_strategies = axl.filtered_strategies(filterstrategies)
    filtered_strategies.remove(axl.Defector)

    opponent_strategies = random.sample(filtered_strategies, num_of_opponents)
    list_of_players = [opponent() for opponent in opponent_strategies]
    list_of_players.append(axl.Defector())

    return list_of_players


################################################################################
def get_game(tournament_rep, player_list, prob_of_game_ending, noise):

    """
    A function which runs a tournament of A Prisoner's Dilemma and returns a dictionary containing the following: 'payoff matrix obtained' (an output from the Axelrod tournament function), 'number of tournament repeats' (from 'tournament_rep'), 'probability of game ending' (from 'prob_of_game_ending) and 'noise' (from 'noise'), where:

    'tournament_rep' is a numeric variable stating how many times the tournament should be executed;

    'player_list' is a list containing instances of specific strategy classes obtained from the Axelrod library;

    'prob_of_game_ending' is a numeric variable between 0 and 1 which states the probability of the tournament ending on any specific turn; and

    'noise' is a numeric variable between 0 and 1 as described on https://axelrod.readthedocs.io/en/stable/tutorials/further_topics/noisy_tournaments.html and https://axelrod.readthedocs.io/en/stable/reference/glossary.html#noise.
    """

    tournament = axl.Tournament(player_list, prob_end=prob_of_game_ending, repetitions=tournament_rep, noise=noise)
    tournament_results = tournament.play(progress_bar=False)

    mean_payoff_matrix = np.array(tournament_results.payoff_matrix)

    get_game_output_dict = {
        'payoff matrix obtained': mean_payoff_matrix,       
        'number of tournament repeats': tournament_rep, 
        'probability of game ending': prob_of_game_ending, 
        'noise': noise
    }
    return get_game_output_dict


################################################################################
def get_prob_of_defection(payoff_matrix, support_enumeration=True):

    """
    A function which computes the Nash Equilibria of the game using one of three algorithms and returns a dictionary of the Nash Equilibria, the maximum and minimum probabilities of defection within the equilibria and whether the game could be degenerate. The input variables are:

    'payoff_matrix', a numpy array containing the payoffs obtained for each action of the game; and

    'support_enumeration', a boolean variable stating whether the support enumeration algorithm (if evaluated true) or the vertex enumeration algorithm (if evaluated False) is used to calculate the Nash equilibria.
    """

    game = nash.Game(payoff_matrix, payoff_matrix.transpose())


    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        if support_enumeration == True:
            nash_equilibria = list(game.support_enumeration())

        else:
            nash_equilibria = list(game.vertex_enumeration())

    
    if len(w) == 0:
        warning_message = None

    else:
        warning_message = str(list(w))


    if (len(nash_equilibria) == 0) or ('-Inf' in nash_equilibria):
        nash_equilibria = None
        prob_of_defection_in_equilibria = None
        least_prob_of_defection_in_equilibria = None
        greatest_prob_of_defection_in_equilibria = None

    else:
        prob_of_defection_in_equilibria = [sigma_1[-1] for sigma_1, _ in nash_equilibria]

        least_prob_of_defection_in_equilibria = min(prob_of_defection_in_equilibria)
        greatest_prob_of_defection_in_equilibria = max(prob_of_defection_in_equilibria)

    get_prob_of_defect_output_dict = {
        'nash equilibria': np.array(nash_equilibria),
        'least prob of defect': least_prob_of_defection_in_equilibria,
        'greatest prob of defect': greatest_prob_of_defection_in_equilibria,
        'warning message': warning_message
    }

    return get_prob_of_defect_output_dict 


################################################################################
def array_to_string(numpy_array):

    """
    A function which converts a numpy array into a space separated string.
    """

    flattened_array = numpy_array.flatten()
    flattened_array_to_string = str(flattened_array).strip('[]')
    return flattened_array_to_string


################################################################################
def write_record(experiment_number, player_strategy_name, is_long_run_time,
    is_stochastic, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix,
    num_of_repetitions, nash_equilibria, least_prob_of_defection,
    greatest_prob_of_defection, noise, warning_message, database_filepath):

    """
    A function which converts the results to a suitable format and writes them to a database, where:

    'experiment_number' is a distinct index for each tournament executed;

    'player_strategy_name' is a string containing the name of the strategy as given in the Axelrod library;

    'is_long_run_time' is a boolean variable which states whether the strategy is considered to take a long time to execute;

    'is_stochastic' is a boolean variable stating whether the strategy is stochastic or deterministic;

    'memory_depth_of_strategy' is a numeric variable which implies how much of a tournament's history does the strategy recall;

    'prob_of_game_ending' is a numeric variable between 0 and 1 which gives the probability of the tournament ending after any turn;
    
    'payoff_matrix' is the matrix containing the mean payoffs obtained from the Axelrod tournament;
    
    'num_of_repetitions' is a numeric variable stating the number of times the tournament was repeated;
    
    'nash_equilibria' is a numpy array containing the nash equilibria obtained using the above 'payoff_matrix';
    
    'least_prob_of_defection' is a numeric variable between 0 and 1 stating the lowest probability of defection appearing in the equilibria;
    
    'greatest_prob_of_defection' is a numeric variable between 0 and 1 stating the highest probability of defection which appeared in the nash equilibria;
    
    'noise' is a numeric variable between 0 and 1 indicating the amount of noise between players during the tournament;
    
    'warning_message' is a string containing any warnings captured during execution of the get_prob_of_defection function; and
    
    'database_filepath' is a string containing the relative path where the database (main.db) file is based.
    """

    database_management_sys = sa.create_engine('sqlite:///' + database_filepath
    + 'main.db')
    connect_dbms_to_db = database_management_sys.connect()

    payoff_matrix_as_string = array_to_string(payoff_matrix)
    
    if nash_equilibria.all() != None:
        num_of_equilibria = len(nash_equilibria)
        nash_equilibria_as_string = array_to_string(nash_equilibria)
    
    else:
        num_of_equilibria = None
        nash_equilibria_as_string = None  

    read_into_sql = """
        INSERT into folk_theorem_experiment 
            (experiment_number, player_strategy_name, is_long_run_time, is_stochastic, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, num_of_equilibria, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, noise, warning_message)
        VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    record = (experiment_number, str(player_strategy_name), is_long_run_time, is_stochastic, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix_as_string, num_of_repetitions, num_of_equilibria, nash_equilibria_as_string, least_prob_of_defection, greatest_prob_of_defection, noise, warning_message)

    connect_dbms_to_db.execute(read_into_sql, record)


################################################################################
def run_experiment(max_num_of_opponents, number_of_player_samples,
    noise_probs, game_ending_probs, tournament_rep, database_filepath, support_enumeration=True):

    """
    A function which runs the experiment and writes the results to a database, where:

    'max_num_of_opponents' is a numeric variable stating the largest number of players who will be competing against the Defector;

    'number_of_player_samples' is a numeric variable indicating how many tournaments with the same number of players should be executed (for each value of noise and each probability of defection);

    'noise_probs' is a list containing numeric variables between 0 and 1 indicating the amount of noise to be included in a tournament;

    'game_ending_probs' is a list containing numeric variables between 0 and 1 indicating the probability of a game ending on any particular turn;

    'tournament_rep' is a numeric variable stating the number of times each distinct tournament should be repeated (allows for the 'smoothing' of the mean payoffs obtained);

    'database_filepath' is a string containing the relative path where the database (main.db) file is based; and

    'support_enumeration' is a boolean variable stating whether the support enumeration algorithm (if evaluated true) or the vertex enumeration algorithm (if evaluated False) is used to calculate the Nash equilibria.
     """
    unique_tournament_identifier = 0
    axl.seed(unique_tournament_identifier)
    for num_of_opponents in range(1, max_num_of_opponents + 1):
        
        for player_sample_repetition in range(1, number_of_player_samples + 1):
            players = who_is_playing(num_of_opponents=num_of_opponents, long_run_strategies=False)

            for noise in noise_probs:
                
                for probability in game_ending_probs:
                    tournament_run = get_game(tournament_rep=tournament_rep, player_list=players, prob_of_game_ending=probability, noise=noise)
                    defection_probs = get_prob_of_defection(payoff_matrix=tournament_run['payoff matrix obtained'], support_enumeration=support_enumeration)
                    
                    for player in players:
                        write_record(experiment_number=unique_tournament_identifier, player_strategy_name=player, is_long_run_time=player.classifier['long_run_time'], is_stochastic=player.classifier['stochastic'], memory_depth_of_strategy=player.classifier['memory_depth'], prob_of_game_ending=tournament_run['probability of game ending'], payoff_matrix=tournament_run['payoff matrix obtained'], num_of_repetitions=tournament_run['number of tournament repeats'], nash_equilibria=defection_probs['nash equilibria'], least_prob_of_defection=defection_probs['least prob of defect'], greatest_prob_of_defection=defection_probs['greatest prob of defect'], noise=tournament_run['noise'], warning_message=defection_probs['warning message'], database_filepath=database_filepath)

                    unique_tournament_identifier += 1
                    axl.seed(unique_tournament_identifier)