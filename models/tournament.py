# -*- coding: utf-8 -*-


class Tournament:
    """Create a tournament"""
    def __init__(self, name, location, date, turns, rounds, players, time,
                 description):
        # turn: a list of matches
        # match: 1 set of 2 players with a result field for each player
        # winner gets 1 pt, loser 0, stalemate 1/2 pt per player
        # match: tuple of two lists, each with 2 items, a ref to an instance
        # of player and a score
        # multiple matches are to be stored as a list on the turn instance

        self.name = name
        self.location = location
        self.date = date
        self.turns = turns
        self.rounds = rounds
        self.players = players
        self.time = time
        self.description = description

    def get_pairs(self):
        ...
