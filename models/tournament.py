# -*- coding: utf-8 -*-

from models.db import Database
from models.match import Match
from models.player import Player
from models.round import Round


class Tournament:
    """Manage a tournament"""

    def __init__(self):
        self._db = Database()
        self.id = None
        self.nb_players = 8
        self.players = []
        self.round = {}
        self.matches = []
        self.time_control = 'bullet'
        self.description = None
        self.name = None
        self.location = None
        self.date = None

    def get_next_id(self, table: str = 'tournament'):
        return self._db.get_next_id(table)

    def create_tournament(self, tournament: dict):
        data = {'id': self._db.get_next_id('tournament')}
        for k, v in tournament.items():
            data[k] = v
        if 'time_control' not in data:
            data['time_control'] = self.time_control
        self.round = Round(1, self.generate_pairs(data['players'])).serialize()
        data['rounds'] = self.round
        self._db.create('tournament', data)

    @staticmethod
    def create_player(player: dict):
        Player(player).create()

    def get_tournaments(self):
        return self._db.read('tournament')

    @staticmethod
    def get_players():
        return Player().get_players()

    def edit_tournament(self, name, location, t_date, **kwargs):
        ...

    def generate_pairs(self, players) -> list:
        if not self.round:
            return self.pair_by_ranking(players)
        else:
            return self.pair_by_points(players)

    def show_latest_pairs(self):
        pairs = []
        latest_round = list(self.round.keys())[-1]
        for item in self.round[latest_round]['matches']:
            pairs.append({
                'player_1': Player(
                    {'id': item['player_1']['id']}).get_player_name(),
                'player_2': Player(
                    {'id': item['player_2']['id']}).get_player_name()
            })
        return pairs

    def pair_by_ranking(self, players):
        players_list = []
        # retrieve players and sort rankings
        for p in players:
            players_list.append(Player().get_rank(p))
        players_list.sort(key=lambda player: player[1])
        half = int(len(players_list) / 2)
        match_list = []
        for p in players_list[:(half)]:
            second_player_index = players_list.index(p) + half
            match = Match(p[0], players_list[second_player_index][0])
            match_list.append(match.serialize())
        return match_list

    def pair_by_points(self, players):
        ...
