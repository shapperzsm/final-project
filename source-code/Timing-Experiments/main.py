import numpy as np
import nashpy as nash
import axelrod as axl
import random
import time
import json



algorithm_to_time_dict = {
    "Support Enumeration": [],
    "Vertex Enumeration": [],
    "Lemke Howson": []
}



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




def probabilities_of_defection(
    tournament_repeat,
    player_list,
    probs_of_game_ending,
    nash_equilibrium_algorithm,
    set_seed,
):
    """
    A function which executes varying tournaments of A Prisoner's Dilemma, each 
    with a distinct probabilistic ending, and then computes the Nash Equilibria 
    of the resulting mean payoff matrix, where:

    'tournament_repeat' is a numeric variable stating how many times each 
    tournament should be played;

    'player_list' is a list containing all the strategies which are competing;

    'probs_of_game_ending' is a list (or numpy array) of values between 0 and 1 
    which state the probability of a specific game ending;

    'nash_equilibrium_algorithm' is a string containing either "Support
    Enumeration", "Vertex Enumeration" or "Lemke Howson". This indicates which
    method will be used in calculating the Nash Equilibria. WARNING - the "Lemke
    Howson" algorithm may not return all Nash Equilibria; and
    
    'set_seed' is a numeric variable which ensures reproducibility if the same
    value is used.

    The output is two lists: the first and second containing the least and 
    greatest probability of defection, respectively, obtained from the Nash 
    Equilibria. 
    """

    least_prob_of_defection_in_equilibria = []
    greatest_prob_of_defection_in_equilibria = []

    for probability in probs_of_game_ending:

        axl.seed(set_seed)

        tournament = axl.Tournament(
            player_list, prob_end=probability, repetitions=tournament_repeat
        )

        tournament_results = tournament.play(progress_bar=False)
        mean_payoff_matrix = np.array(tournament_results.payoff_matrix)

        game = nash.Game(mean_payoff_matrix, mean_payoff_matrix.transpose())

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

        prob_of_defection_in_equilibria = [
            sigma_1[-1] for sigma_1, _ in nash_equilibria
        ]

        least_prob_of_defection_in_equilibria.append(
            min(prob_of_defection_in_equilibria)
        )

        greatest_prob_of_defection_in_equilibria.append(
            max(prob_of_defection_in_equilibria)
        )

    return least_prob_of_defection_in_equilibria, greatest_prob_of_defection_in_equilibria




def same_strategies_repeat(same_strategies_rep, players, number_of_repeats, game_end_probs, algorithm, execution_time):
    """
    A function which records the execution time of A Prisoner's Dilemma tournament for the same strategies a certain number of times, where:

    'same_strategies_rep' is a numeric variable stating the number of times the timing experiment should be repeated with the chosen strategies;

    'players' is a list containing the names of the strategies, obtained using the who_is_playing function;

    'number_of_repeats' is the number of times the tournament should be executed during one iteration of the timing experiment;

    'game_end_probs' is a list containing numeric variables between 0 and 1, indicating the probabilities of the tournament ending;

    'algorithm' is one of the three algorithms used to calculate the Nash
    Equilibria of the obtained payoff matrix from the tournaments, taken from
    the algorithm_to_time_dict;
    
    'execution_time' is an empty list.
    """

    for same_opponents_repeat in range(same_strategies_rep):

        #print(same_opponents_repeat)
        #print(players)

        initial_time = time.perf_counter()
        probabilities_of_defection(tournament_repeat=number_of_repeats, player_list=players, probs_of_game_ending=game_end_probs, nash_equilibrium_algorithm=str(algorithm), set_seed=123)
        final_time = time.perf_counter()
        execution_time.append(final_time - initial_time)
            
        #print(execution_time)
    return execution_time
 



def same_num_of_players_rep(same_player_rep, number_of_opponents, same_strategies_rep, number_of_repeats, game_end_probs, algorithm, average_running_time_for_same_players=[]):

    """
    A function which executes the 'same_strategies_repeat' function a certain number of times and from this calculates the average running time for each different set of strategies of the same size, where:

    'same_player_rep' is a numeric variable stating how many different sets,
    with the same number of strategies, will be used in the experiment;
    
    'number_of_opponents' is a numeric variable stating how many opponents the
    axl.Defector() will have;

    'same_strategies_rep' is a numeric variable indicating the number of times the experiment will be executed for one particular set of strategies;

    'number of repeats' is a numeric variable stating how many times a single tournament will be executed;

    'game_end_probs' is a list containing numeric variables, between 0 and 1, indicating the probabilities of the tournament ending;

    'algorithm' is one of the three algorithms used to calculate the Nash Equilibria of the obtained payoff matrix from the tournaments, taken from the algorithm_to_time_dict; and

    'average_running_time_for_same_players' is an empty list.
    """

    for same_number_of_players_repeat in range(same_player_rep):
        
        #print(same_number_of_players_repeat)

        players = who_is_playing(num_of_opponents=number_of_opponents)
        
        #print(players)
        
        
        same_strategy_time = same_strategies_repeat(same_strategies_rep=same_strategies_rep, players=players, number_of_repeats=number_of_repeats, game_end_probs=game_end_probs, algorithm=algorithm, execution_time=[])

        print("Finished inner for loop!")

        mean_execution_time_for_same_players = sum(same_strategy_time) / len(same_strategy_time)
        average_running_time_for_same_players.append(mean_execution_time_for_same_players)

        #print(average_running_time_for_same_players)
    return average_running_time_for_same_players




def run_tournament_over_diff_group_sizes(max_num_of_opponents, same_player_rep, number_of_opponents, same_strategies_rep, number_of_repeats, game_end_probs, algorithm, average_running_time=[]):

    """
    A function which executes the Prisoner's Dilemma tournament for differing numbers of opponents against axl.Defector, where:

    'max_num_of_opponents' is a numeric variable which indicates the maximum number of opponents axl.Defector will have;

    'same_player_rep' is a numeric variable stating how many different sets,
    with the same number of strategies, will be used in the experiment;
    
    'number_of_opponents' is a numeric variable stating how many opponents the
    axl.Defector() will have;

    'same_strategies_rep' is a numeric variable indicating the number of times the experiment will be executed for one particular set of strategies;

    'number of repeats' is a numeric variable stating how many times a single tournament will be executed;

    'game_end_probs' is a list containing numeric variables, between 0 and 1, indicating the probabilities of the tournament ending;

    'algorithm' is one of the three algorithms used to calculate the Nash
    Equilibria of the obtained payoff matrix from the tournaments, taken from
    the algorithm_to_time_dict; and
    
    'average_running_time' is an empty list.

    This function also continually saves the dictionary containing the execution
    times to a json file.
    """

    while number_of_opponents <= max_num_of_opponents:
    
        #print(number_of_opponents)

        
        average_time_same_num = same_num_of_players_rep(same_player_rep=same_player_rep, number_of_opponents=number_of_opponents, same_strategies_rep=same_strategies_rep, number_of_repeats=number_of_repeats, game_end_probs=game_end_probs, algorithm=algorithm, average_running_time_for_same_players=[])
        
        print("Finished outer for loop!")

        mean_execution_time_for_same_num = sum(average_time_same_num) / len(average_time_same_num)
        average_running_time.append(mean_execution_time_for_same_num)

        #print(average_running_time)

        json_file = open("timings-dict1.json", "w")
        algorithm_to_time_dict[algorithm].append(mean_execution_time_for_same_num)
        save_to_json = json.dumps(algorithm_to_time_dict)
        json_file.write(save_to_json)
        json_file.close()

        number_of_opponents += 1
    return average_running_time




def repeating_for_all_algorithm(max_num_of_opponents, same_player_rep, same_strategies_rep, number_of_repeats, game_ending_probs, alg_dict=algorithm_to_time_dict, number_of_opponents=1):

    """
    A function which runs the repeated timing experiments for all three
    algorithms in the algorithm_to_time_dict, where:

    'max_num_of_opponents' is a numeric variable which indicates the maximum number of opponents axl.Defector will have;

    'same_player_rep' is a numeric variable stating how many different sets,
    with the same number of strategies, will be used in the experiment;

    'same_strategies_rep' is a numeric variable indicating the number of times the experiment will be executed for one particular set of strategies;

    'number of repeats' is a numeric variable stating how many times a single tournament will be executed;

    'game_end_probs' is a list containing numeric variables, between 0 and 1, indicating the probabilities of the tournament ending;

    'alg_dict' is a dictionary containing as keys the three algorithms for
    calculating Nash Equilibria, along with an empty list in which the execution
    times will be inputted; 
    
    'number_of_opponents' is the minimum number of opponents that the Defector
    will play against;
    """

    for algorithm in alg_dict:
        print(algorithm)
        run_tournament_over_diff_group_sizes(max_num_of_opponents=max_num_of_opponents, same_player_rep=same_player_rep, number_of_opponents=number_of_opponents, same_strategies_rep=same_strategies_rep, number_of_repeats=number_of_repeats, game_end_probs=game_ending_probs, algorithm=algorithm)
        print("Finished while loop!")
    return algorithm_to_time_dict


#ending_probabilities = np.linspace(0.001, 1-0.001, 50)
ending_probabilities = np.linspace(0.001, 1-0.001, 10)

print("I have started...")

#repeating_for_all_algorithm(max_num_of_opponents=11, same_player_rep=10,
#same_strategies_rep=5, number_of_repeats=50,
#game_ending_probs=ending_probabilities)

#repeating_for_all_algorithm(max_num_of_opponents=11, same_player_rep=10, same_strategies_rep=5, number_of_repeats=50, game_ending_probs=ending_probabilities, alg_dict=["Lemke Howson", "Vertex Enumeration"])

#repeating_for_all_algorithm(max_num_of_opponents=11, same_player_rep=5,same_strategies_rep=2, number_of_repeats=10,game_ending_probs=ending_probabilities)

repeating_for_all_algorithm(max_num_of_opponents=9, same_player_rep=5, same_strategies_rep=2, number_of_repeats=10, game_ending_probs=ending_probabilities, alg_dict=["Lemke Howson", "Vertex Enumeration"])

print("I have finished!")