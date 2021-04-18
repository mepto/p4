# -*- coding: utf-8 -*-

from models.db import Database
from models.match import Match
from models.player import Player
from models.round import Round


class Tournament:
    """Manage a tournament"""

    def __init__(self, tournament: dict = {}):
        self._db = Database()
        self.id = tournament['id'] if 'id' in tournament else \
            self._db.get_next_id('tournament')
        self.nb_players = 8
        self.players = tournament['players'] if 'players' in tournament else []
        self.matches = []
        if 'rounds' not in tournament:
            self.rounds = {}
        else:
            self.rounds = tournament['rounds']
            for item in self.rounds:
                self.matches += self.rounds[item]['matches']
        self.time_control = 'bullet' if 'time_control' not in tournament else \
            tournament['time_control']
        self.description = tournament['description'] if 'description' in \
                                                        tournament else None
        self.name = tournament['name'] if 'name' in tournament else None
        self.location = None if 'location' not in tournament else \
            tournament['location']
        self.date = tournament['date'] if 'date' in tournament else None

    def get_next_id(self, table: str = 'tournament') -> int:
        return self._db.get_next_id(table)

    def create_tournament(self, tournament: dict):
        data = {'id': self._db.get_next_id('tournament')}
        for k, v in tournament.items():
            data[k] = v
        if 'time_control' not in data or not data['time_control']:
            data['time_control'] = self.time_control
        self.rounds = Round(1, self.generate_pairs(data['players'])).serialize()
        data['rounds'] = self.rounds
        self._db.create('tournament', data)

    @staticmethod
    def create_player(player: dict):
        Player(player).create()

    def get_tournaments(self) -> list:
        return self._db.read('tournament')

    def get_players(self, tournament_id: int = None, order: str = None) -> list:
        all_players = Player().get_players()  # list of dicts
        if tournament_id:
            tournament = self._db.read('tournament', **{'id': tournament_id})
            for player in all_players:
                if player['id'] not in tournament[0]['players']:
                    all_players.remove(player)
        if order == 'alpha':
            all_players.sort(key=lambda item: item.get('last_name').upper())
        elif order == 'ranking':
            all_players.sort(key=lambda item: item.get('ranking'))
        return all_players

    def get_matches(self, tournament_id: int = None) -> list:
        if tournament_id:
            db_data = self._db.read('tournament', **{'id': tournament_id})
            tournament = Tournament(db_data[0])
            matches = []
            for pair in tournament.matches:
                match = {}
                count = 1
                for player in pair:
                    name = Player({'id': player[0]}).get_player_name()
                    score = player[1]
                    current_player = f"Player {count}"
                    match[current_player] = f"{name}, score {score}"
                    count += 1
                matches.append(match)
            return matches
        return [{'matches': 'Nothing to report'}]

    def get_rounds(self, tournament_id: int = None) -> list:
        if tournament_id:
            data = []
            db_data = self._db.read('tournament', **{'id': tournament_id})
            tournament = Tournament(db_data[0])
            rounds = tournament.rounds
            for round in rounds:
                current_round = {}
                current_round['name'] = round
                for item in rounds[round]:
                    current_round[item] = rounds[round][item]
                data.append(current_round)
            return data
        return [{'rounds': 'Nothing to report'}]

    def enter_match_results(self, name, location, t_date, **kwargs):
        ...

    def generate_pairs(self, players) -> list:
        if not self.rounds:
            return self.pair_by_ranking(players)
        else:
            return self.pair_by_points(players)

    def show_latest_pairs(self) -> list:
        pairs = []
        latest_round = list(self.rounds.keys())[-1]
        for item in self.rounds[latest_round]['matches']:
            pairs.append({
                'player_1': Player(
                    {'id': item[0][0]}).get_player_name(),
                'player_2': Player(
                    {'id': item[1][0]}).get_player_name()
            })
        return pairs

    def pair_by_ranking(self, players) -> list:
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
