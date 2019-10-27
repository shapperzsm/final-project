import numpy as np
import nashpy as nash
import axelrod as axl
import random

####################################################
def who_is_playing(num_of_opponents, long_run_strategies=False):
    """
    A function to choose which strategies will be playing against the Defector.

    'num_of_opponents' is a numeric variable which states how many players will 
    be competing (EXCLUDING the Defector).

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

###################################################
def get_game(tournament_repeat, player_list, prob_of_game_ending, set_seed, noise):

    """
    A function which executes a tournament of A Prisoner's Dilemma and returns the mean payoff matrix obtained using the Axelrod library, where:

    'tournament_repeat' is a numeric variable stating how many times each tournament should be played;

    'player_list' is a list containing instances of specific strategy classes obtained from the Axelrod library;

    'prob_of_game_ending' is a numeric variable between 0 and 1 which states the probability of the tournament ending on any specific turn;

    'seet_seed' is a numeric variable which ensures reproducibility if the same value is used; and

    'noise' is a numeric variable between 0 and 1 which indicates how much noise should be included in the tournament.
    """

    axl.seed(set_seed)

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

######################################################
def get_prob_of_defection(payoff_matrix, nash_equilibrium_algorithm):

    """
    A function which computes the Nash Equilibria of the game using one of three algorithms and returns a dictionary of the Nash Equilibria along with the maximum and minimum probabilities of defection within the equilibria. The input variables are:

    'payoff_matrix', a numpy array containing the payoffs obtained for each action of the game; and

    'nash_equilibrium_algorithm', a string containing either "Support
    Enumeration", "Vertex Enumeration" or "Lemke Howson". This indicates which
    method will be used in calculating the Nash Equilibria.
    """

    game = nash.Game(payoff_matrix, payoff_matrix.transpose())

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

    prob_of_defection_in_equilibria = [sigma_1[-1] for sigma_1, _ in nash_equilibria]

    least_prob_of_defection_in_equilibria = min(prob_of_defection_in_equilibria)
    greatest_prob_of_defection_in_equilibria = max(prob_of_defection_in_equilibria)

    get_prob_of_defect_output_dict = {
        'nash equilibria': nash_equilibria,
        'least prob of defect': least_prob_of_defection_in_equilibria,
        'greatest prob of defect': greatest_prob_of_defection_in_equilibria
    }

    return get_prob_of_defect_output_dict      

####################################################
def array_to_string(numpy_array):

    """
    A function which converts a numpy array into a space separated string.
    """

    flattened_array = numpy_array.flatten()
    flattened_array_to_string = str(flattened_array).strip('[]')
    return flattened_array_to_string



