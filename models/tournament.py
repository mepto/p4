# -*- coding: utf-8 -*-
from datetime import date

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
        self.players = []
        self.turns = {}
        self.nb_rounds = {}
        self.rounds = []
        self.time = None
        self.description = None
        self.name = None
        self.location = None
        self.date = None

    def create_tournament(self, tournament: dict):
        self._db.create('tournament', {
            # TODO: get last id in table + 1
            'id': len(self._db.tournament_table) + 1,
            'name': tournament['name'],
            'location': tournament['location'],
            'date': tournament['date']})

    def create_player(self, player: dict):
        Player(player).create()

    def get_tournaments(self):
        return self._db.read('tournament')

    def get_players(self):
        return Player().get_players()

    def save_new_entry(self, name, location, t_date, **kwargs):
        current_items = {name: name, location: location, date: t_date}
        for key, value in kwargs:
            current_items[key] = value

        self._db.insert(current_items)

    def update_entry(self, name, location, t_date, **kwargs):
        ...

    def get_pairs(self):
        ...
