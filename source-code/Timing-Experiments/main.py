import numpy as np     
import nashpy as nash
import axelrod as axl
import random




def who_is_playing(num_of_opponents, long_run_strategies = False):
    """
    A function to choose which strategies will be playing against the Defector.

    'num_of_opponents' is a numeric variable which states how many players will be competing (EXCLUDING the  Defector).

    'long_run_strategies' is a Boolean variable which states whether strategies which have a long running time should be included in the competitors or not. It has a default value of False.

    A list containing the selected strategies is returned.
    """

    if long_run_strategies == True:
        filterstrategies = {       
        'manipulates_state': False,
        'manipulates_source': False,
        'inspects_source': False
        }
    else:
        filterstrategies = {
        'long_run_time': False,
        'manipulates_state': False,
        'manipulates_source': False,
        'inspects_source': False
        }   

    filtered_strategies = axl.filtered_strategies(filterstrategies)
    filtered_strategies.remove(axl.Defector)

    opponent_strategies = random.sample(filtered_strategies, num_of_opponents)

    list_of_players = [opponent_strategies[i]() for i in range(num_of_opponents)]
    list_of_players.append(axl.Defector())

    return list_of_players





def probabilities_of_defection(num_of_repeats, player_list, probs_of_game_ending, nash_equilibrium_algorithm, set_seed):
    """
    A function which executes varying tournaments of A Prisoner's Dilemma, each with a distinct probabilistic ending, and then computes the Nash Equilibria of the resulting mean payoff matrix, where:

    'num_of_repeats' is a numeric variable stating how many times each tournament should be played;

    'player_list' is a list containing all the strategies which are competing;

    'probs_of_game_ending' is a list (or numpy array) of values between 0 and 1 which state the probability of a specific game ending;

    'nash_equilibrium_algorithm' is a string containing either "Support
    Enumeration", "Vertex Enumeration" or "Lemke Howson". This indicates which
    method will be used in calculating the Nash Equilibria. WARNING - the "Lemke
    Howson" algorithm may not return all Nash Equilibria; and
    
    'set_seed' is a numeric variable which ensures reproducibility if the same
    value is used.

    The output is two lists: the first and second containing the least and greatest probability of defection, respectively, obtained in the Nash Equilibria. 
    """

    least_prob_of_defection_in_equilibria = []
    greatest_prob_of_defection_in_equilibria = []

    for probability in probs_of_game_ending:
        
        axl.seed(set_seed)

        tournament = axl.Tournament(player_list, prob_end=probability, repetitions=num_of_repeats)
        
        tournament_results = tournament.play(progress_bar=False)
        mean_payoff_matrix = np.array(tournament_results.payoff_matrix)
        
        game = nash.Game(mean_payoff_matrix, mean_payoff_matrix.transpose())


        if nash_equilibrium_algorithm == 'Support Enumeration':
            least_prob_of_defection_in_equilibria.append(min([sigma_1[-1] for sigma_1, _ in game.support_enumeration()]))
            greatest_prob_of_defection_in_equilibria.append(max([sigma_1[-1] for sigma_1, _ in game.support_enumeration()]))
    
        elif nash_equilibrium_algorithm == 'Vertex Enumeration':
            least_prob_of_defection_in_equilibria.append(min([sigma_1[-1] for sigma_1, _ in game.vertex_enumeration()]))
            greatest_prob_of_defection_in_equilibria.append(min([sigma_1[-1] for sigma_1, _ in game.vertex_enumeration()]))
            
        elif nash_equilibrium_algorithm == 'Lemke Howson':
            least_prob_of_defection_in_equilibria.append(min([sigma_1[-1] for sigma_1, _ in game.lemke_howson_enumeration()]))
            greatest_prob_of_defection_in_equilibria.append(min([sigma_1[-1] for sigma_1, _ in game.lemke_howson_enumeration()]))
    return least_prob_of_defection_in_equilibria, greatest_prob_of_defection_in_equilibria
