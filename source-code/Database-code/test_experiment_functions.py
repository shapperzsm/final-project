import experiment_functions as expfun
import axelrod as axl
import nashpy as nash
import numpy as np

def test_who_is_playing():
    for num_of_opponents in range(1, 10):
        players = expfun.who_is_playing(num_of_opponents)
        assert len(players) == num_of_opponents + 1
        for player in players:
            assert player.classifier["long_run_time"] == False



def test_get_game():
    game = expfun.get_game(4, [axl.Cooperator(), axl.TitForTat(), axl.Defector()], 0.2, 0.7)
    type(game) == type(dict())
    assert game['payoff matrix obtained'].shape ==  (3, 3)      
    assert game['number of tournament repeats'] == 4
    assert game['probability of game ending'] == 0.2
    assert game['noise'] == 0.7


def test_get_prob_of_defection():
    matrix = np.array([[3, 0], [5, 1]])
    nash_eq = list(nash.Game(matrix, matrix.transpose()).support_enumeration())
    defection_prob = expfun.get_prob_of_defection(np.array([[3, 0], [5, 1]]))
    assert len(defection_prob['nash equilibria']) == len(nash_eq)
    assert defection_prob['least prob of defect'] == min([sigma_1[-1] for sigma_1, _ in nash_eq])
    assert defection_prob['greatest prob of defect'] == max([sigma_1[-1] for sigma_1, _ in nash_eq])
    assert type(defection_prob['could be degenerate']) == type(True)


def test_array_to_string():
    string_array = expfun.array_to_string(np.array([[3, 0], [5, 1]]))
    assert type(string_array) == type("this is a test")
    assert string_array == "3 0 5 1"
