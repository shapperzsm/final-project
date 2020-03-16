import database_code as dbcode
import axelrod as axl
import nashpy as nash
import numpy as np
import os
import sqlalchemy as sql
import pandas as pd


def test_create_directory():
    """
    checks if the folder structure is created.
    """
    dbcode.create_directory()
    assert os.path.isdir("data/se")
    assert os.path.isdir("data/ve")


def test_create_database():
    """
    checks the database file is created.
    """
    dbcode.create_database("data/se")
    database_management_sys = sql.create_engine("sqlite:///data/se/main.db")
    assert os.path.isfile("data/se/main.db")


def test_who_is_playing():
    """
    checks the 'who is playing function': selects the correct number of
    strategies from the Axelrod library; returns a list; always contains the
    Defector strategy; and the strategies are not classed as 'long running'.
    """
    for num_of_opponents in range(1, 10):
        players = dbcode.who_is_playing(num_of_opponents)
        assert len(players) == num_of_opponents + 1
        assert type(players) == type(list())
        assert axl.Defector() in players
        for player in players:
            assert player.classifier["long_run_time"] == False


def test_array_to_string():
    string_array = dbcode.array_to_string(np.array([[3, 0], [5, 1]]))
    assert type(string_array) == type("this is a test")
    assert string_array == "3 0 5 1"
