import database_code as dbcode
import axelrod as axl
import nashpy as nash
import numpy as np
import sqlalchemy as sql
import pytest


@pytest.mark.parametrize(
    "num_of_opponents, tournament_rep, prob_of_game_ending, noise",
    [(2, 100, 0.4, 0.0), (5, 100, 0.7, 0.3), (7, 100, 0.85, 0.0), (3, 100, 0.2, 0.6)],
)
def test_get_game(num_of_opponents, tournament_rep, prob_of_game_ending, noise):
    """
    checking the tournament is run correctly & the required output is as expected
    """
    players = dbcode.who_is_playing(num_of_opponents)
    game = dbcode.get_game(tournament_rep, players, prob_of_game_ending, noise)
    assert type(game) == type(dict())
    assert type(game["payoff matrix obtained"]) == type(np.array([[3, 5], [5, 1]]))
    assert game["payoff matrix obtained"].shape == (len(players), len(players))
    assert game["number of tournament repeats"] == tournament_rep
    assert game["probability of game ending"] == prob_of_game_ending
    assert game["noise"] == noise


@pytest.mark.parametrize(
    "num_of_opponents, tournament_rep, prob_of_game_ending, noise",
    [(2, 100, 0.4, 0.0), (5, 100, 0.7, 0.3), (7, 100, 0.85, 0.0), (3, 100, 0.2, 0.6)],
)
def test_get_prob_of_defection(
    num_of_opponents, tournament_rep, prob_of_game_ending, noise
):
    """
    checking the equilibria and probabilities of defection obtained using the function 'get_prob_of_defection'
    and separately via nashpy are equivalent.
    """
    players = dbcode.who_is_playing(num_of_opponents)
    game = dbcode.get_game(tournament_rep, players, prob_of_game_ending, noise)
    matrix = game["payoff matrix obtained"]
    nash_eq = list(nash.Game(matrix, matrix.transpose()).support_enumeration())
    defection_prob = dbcode.get_prob_of_defection(game["payoff matrix obtained"])
    assert len(defection_prob["nash equilibria"]) == len(nash_eq)
    assert defection_prob["least prob of defect"] == min(
        [sigma_1[-1] for sigma_1, _ in nash_eq]
    )
    assert defection_prob["greatest prob of defect"] == max(
        [sigma_1[-1] for sigma_1, _ in nash_eq]
    )
    assert type(defection_prob["warning message"]) == type("this is a test")
    assert type(defection_prob) == type(dict())
