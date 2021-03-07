# -*- coding: utf-8 -*-
from models.db import Database


class Player:
    """Create a player"""
    def __init__(self, player: dict = {}):
        if player:
            self.last_name = player['last_name']
            self.first_name = player['first_name']
            self.dob = player['dob']
            self.gender = player['gender']
            self.ranking = player['ranking']
        # TODO: cache db and use cached db
        self._db = Database()

    def create(self):
        self._db.create('player', {
            'id': self._db.get_next_id('player'),
            'last_name': self.last_name,
            'first_name': self.first_name,
            'dob': self.dob,
            'gender': self.gender,
            'ranking': self.ranking})

    def get_players(self):
        return self._db.read('player')
