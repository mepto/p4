# -*- coding: utf-8 -*-


class Player:
    """Create a player"""
    def __init__(self, last_name, first_name, dob, gender, ranking=None):
        self.last_name = last_name
        self.first_name = first_name
        self.dob = dob
        self.gender = gender
        self.ranking = ranking
