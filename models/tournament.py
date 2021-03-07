# -*- coding: utf-8 -*-

from models.db import Database
from models.player import Player


class Tournament:
    """Manage a tournament"""

    def __init__(self):
        # turn: a list of matches
        # match: 1 set of 2 players with a result field for each player
        # winner gets 1 pt, loser 0, stalemate 1/2 pt per player
        # match: tuple of two lists, each with 2 items, a ref to an instance
        # of player and a score
        # multiple matches are to be stored as a list on the turn instance
        self._db = Database()
        self.id = None
        self.nb_players = 8
        self.players = []
        self.turns = {}
        self.nb_rounds = {}
        self.rounds = []
        self.time_control = 'bullet'
        self.description = None
        self.name = None
        self.location = None
        self.date = None

    def get_next_id(self, table: str = 'tournament'):
        return self._db.get_next_id(table)

    def create_tournament(self, tournament: dict):
        data = {}
        data['id'] = self._db.get_next_id('tournament')
        for k, v in tournament.items():
            data[k] = v
        if 'time_control' not in data:
            data['time_control'] = self.time_control
        self._db.create('tournament', data)

    def create_player(self, player: dict):
        Player(player).create()

    def get_tournaments(self):
        return self._db.read('tournament')

    def get_players(self):
        return Player().get_players()

    def update_entry(self, name, location, t_date, **kwargs):
        ...

    def get_pairs(self):
        ...
