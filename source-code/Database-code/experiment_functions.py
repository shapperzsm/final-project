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
    CREATE TABLE folk_theorem_experiment (
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
        could_be_degenerate         BOOLEAN NOT NULL,
        
        CONSTRAINT folk_theorem_experiment_pk PRIMARY KEY (experiment_number, player_strategy_name),
        CONSTRAINT prob_of_game_ending_ck CHECK (prob_of_game_ending BETWEEN 0 AND 1),
        CONSTRAINT least_prob_of_defection_ck CHECK (least_prob_of_defection BETWEEN 0 AND 1)
        CONSTRAINT greatest_prob_of_defection_ck CHECK (greatest_prob_of_defection BETWEEN 0 AND 1)
        CONSTRAINT noise_ck CHECK (noise BETWEEN 0 AND 1)
    )
    """
    connect_dbms_to_db.execute(create_table)
    

################################################################################
def who_is_playing(num_of_opponents, seed, long_run_strategies=False):
    """
    A function to choose which strategies will be playing against the Defector, where:

    'num_of_opponents' is a numeric variable which states how many players will 
    be competing (EXCLUDING the Defector);

    'seed' is a numeric variable which ensures reproducibility if the same value is used; and

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

    axl.seed(seed)
    opponent_strategies = random.sample(filtered_strategies, num_of_opponents)
    list_of_players = [opponent() for opponent in opponent_strategies]
    list_of_players.append(axl.Defector())

    return list_of_players

################################################################################
def get_game(tournament_repeat, player_list, prob_of_game_ending, set_seed, noise):

    """
    A function which executes a tournament of A Prisoner's Dilemma and returns the mean payoff matrix obtained using the Axelrod library, where:

    'tournament_repeat' is a numeric variable stating how many times each tournament should be played;

    'player_list' is a list containing instances of specific strategy classes obtained from the Axelrod library;

    'prob_of_game_ending' is a numeric variable between 0 and 1 which states the probability of the tournament ending on any specific turn;

    'seet_seed' is a numeric variable which ensures reproducibility if the same value is used; and

    'noise' is a numeric variable between 0 and 1 which indicates how much noise should be included in the tournament.
    """

    tournament = axl.Tournament(player_list, prob_end=prob_of_game_ending, repetitions=tournament_repeat, noise=noise)
    tournament_results = tournament.play(progress_bar=False)

    mean_payoff_matrix = np.array(tournament_results.payoff_matrix)

    get_game_output_dict = {
        'payoff matrix obtained': mean_payoff_matrix,       
        'number of tournament repeats': tournament_repeat, 
        'probability of game ending': prob_of_game_ending, 
        'noise': noise
    }
    return get_game_output_dict

################################################################################
def get_prob_of_defection(payoff_matrix, nash_equilibrium_algorithm):

    """
    A function which computes the Nash Equilibria of the game using one of three algorithms and returns a dictionary of the Nash Equilibria, the maximum and minimum probabilities of defection within the equilibria and whether the game could be degenerate. The input variables are:

    'payoff_matrix', a numpy array containing the payoffs obtained for each action of the game; and

    'nash_equilibrium_algorithm', a string containing either "Support
    Enumeration", "Vertex Enumeration" or "Lemke Howson". This indicates which
    method will be used in calculating the Nash Equilibria.
    """

    game = nash.Game(payoff_matrix, payoff_matrix.transpose())


    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
    
        if nash_equilibrium_algorithm == "Support Enumeration":
            nash_equilibria = list(game.support_enumeration())
            #print(nash_equilibria)

        elif nash_equilibrium_algorithm == "Vertex Enumeration":
            nash_equilibria = list(game.vertex_enumeration())
            #print(nash_equilibria)

        elif nash_equilibrium_algorithm == "Lemke Howson":
            nash_equilibria = list(game.lemke_howson_enumeration())
            #print(nash_equilibria)

        else:
            raise Exception(
                "nash_equilibrium_algorithm should be one of ['Support Enumeration', 'Vertex Enumeration', 'Lemke Howson']"
            )
    
    if len(w) == 0:
        perhaps_degenerate = False

    else:
        perhaps_degenerate = "degenerate" in str(w[0].message)


    if len(nash_equilibria) == 0:
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
        'could be degenerate': perhaps_degenerate
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
    greatest_prob_of_defection, noise, could_be_degenerate, database_filepath):

    """
    A function which converts the results to a suitable format and writes them to a database, where:

    'experiment_number' is a distinct index for each tournament executed;

    'player_strategy_name' is a string containing the name of the strategy as given in the Axelrod library;

    'is_long_run_time' is a boolean variable which states whether the strategy is considered to take a long time to execute;

    'is_stochastic' is a boolean variable stating whether the strategy is stochastic or deterministic;

    'memory_depth_of_strategy' is a numeric variable which implies how much of a tournament's history does the strategy recall;

    'prob_of_game_ending' is a numeric variable between 0 and 1 which gives the probability of the tournament ending after any turn;
    
    'payoff_matrix' is the matrix containing the mean payoffs obtained from the tournament;
    
    'num_of_repetitions' is a numeric variable stating the number of times the tournament was repeated;
    
    'nash_equilibria' is a numpy array containing the nash equilibria obtained using the above 'payoff_matrix';
    
    'least_prob_of_defection' is a numeric variable between 0 and 1 stating the lowest probability of defection appearing in the equilibria;
    
    'greatest_prob_of_defection' is a numeric variable between 0 and 1 stating the highest probability of defection which appeared in the nash equilibria;
    
    'noise' is a numeric variable between 0 and 1 indicating the amount of noise between players during the tournament;
    
    'could_be_degenerate' is a boolean variable which highlights whether, during the execution of the algorithms for calculating the Nash equilibria, a warning was produced indicating that the game could possibly be degenerate; and
    
    'database_filepath' is a string containing the relative path where the database (.db) file is based.
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
            (experiment_number, player_strategy_name, is_long_run_time, is_stochastic, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix, num_of_repetitions, num_of_equilibria, nash_equilibria, least_prob_of_defection, greatest_prob_of_defection, noise, could_be_degenerate)
        VALUES 
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    record = (experiment_number, str(player_strategy_name), is_long_run_time, is_stochastic, memory_depth_of_strategy, prob_of_game_ending, payoff_matrix_as_string, num_of_repetitions, num_of_equilibria, nash_equilibria_as_string, least_prob_of_defection, greatest_prob_of_defection, noise, could_be_degenerate)

    connect_dbms_to_db.execute(read_into_sql, record)

################################################################################
def run_experiment(max_num_of_opponents, tournament_repeats,
    game_ending_probs, seed, noise, database_filepath,
    experiment_num = 1, support_enumeration=True):

    """
    A function which runs the experiment and writes the results to a database, where:

    'max_num_of_opponents' is a numeric variable stating the maximum number of players that will compete against the Defector;

    'tournament_repeats' is a numeric variable stating the number of times the Axelrod tournament will be executed, to 'smooth' out the mean payoff values which will be used to find the Nash Equilibria;

    'game_ending_probs' is a list containing numeric variables between 0 and 1 indicating the probability that the tournament ends after any given turn;

    'seed' is a numeric variable which ensures reproducibility if the same value is used;

    'noise' is a numeric variable between 0 and 1 which indicates how much stochasticity should be included in any particular choice of action for each player (taken from Axelrod);

    'database_filepath' is a string containing the relative path where the database file will be stored;

    'num_of_opponents' is a numeric variable stating the minimum number of players that will compete against the Defector;
    
    'experiment_num' is a numeric variable which states what number the experiments should start being enumerated at; and
    
    'support_enumeration' is a boolean variable where True (default) implies that the 'support enumeration algorithm' is used to find the Nash Equilibria, otherwise the 'vertex enumeration algorithm' is used.
    """
    unique_tournament_identifier = 0
    for num_of_opponents in range(1, max_num_of_opponents + 1):
        
        axl.seed(num_of_opponents)
        for player_sample_repetition in range(1, number_of_player_samples + 1):
            players = who_is_playing(num_of_opponents=num_of_opponents, long_run_strategies=False)

            for noise in noise_probs:
            for probability in game_ending_probs:

                
                tournament_run = get_game(tournament_repeat=tournament_repeats, player_list=players, prob_of_game_ending=probability, noise=noise)


                if support_enumeration == True:
                    defection_probs = get_prob_of_defection(payoff_matrix=tournament_run['payoff matrix obtained'], nash_equilibrium_algorithm="Support Enumeration")
                    
                else:
                    defection_probs = get_prob_of_defection(payoff_matrix=tournament_run['payoff matrix obtained'], nash_equilibrium_algorithm="Vertex Enumeration")

                for player in players:
                    write_record(experiment_number=experiment_num, player_strategy_name=player, is_long_run_time=player.classifier['long_run_time'], is_stochastic=player.classifier['stochastic'], memory_depth_of_strategy=player.classifier['memory_depth'], prob_of_game_ending=tournament_run['probability of game ending'], payoff_matrix=tournament_run['payoff matrix obtained'], num_of_repetitions=tournament_run['number of tournament repeats'], nash_equilibria=defection_probs['nash equilibria'], least_prob_of_defection=defection_probs['least prob of defect'], greatest_prob_of_defection=defection_probs['greatest prob of defect'], noise=tournament_run['noise'], could_be_degenerate=defection_probs['could be degenerate'], database_filepath=database_filepath)

                unique_tournament_identifier += 1
