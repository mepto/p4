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
                self.matches.append(self.rounds[item]['matches'])
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
        for key, value in tournament.items():
            data[key] = value
        if 'time_control' not in data or not data['time_control']:
            data['time_control'] = self.time_control
        self.rounds = Round(1,
                            self.generate_pairs(data['players'])).serialize()
        data['rounds'] = self.rounds
        self._db.create('tournament', data)

    @staticmethod
    def create_player(player: dict):
        Player(player).create()

    def get_tournaments(self) -> list:
        return self._db.read('tournament')

    def get_players(self, tournament_id: int = None,
                    order: str = None) -> list:
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

    def get_matches(self, tournament_id: int = None,
                    last_round: bool = False) -> list:
        no_results = [{'matches': 'Nothing to report'}]
        if tournament_id:
            tournament_data = self._db.read('tournament',
                                            **{'id': tournament_id})[0][0]
            rounds = tournament_data['rounds']
            matches = []
            results = []
            if last_round:
                current_round = next(
                    reversed(rounds.keys()))
                matches = rounds[current_round]['matches']
            else:
                for item in rounds:
                    for match in rounds[item]['matches']:
                        matches.append(match)
            match_id = 1
            for pair in matches:
                match = {}
                count = 1
                match['match'] = match_id
                for item in pair:
                    name = Player({'id': item[0]}).get_player_name()
                    score = item[1]
                    current_player = f"Player {count}"
                    match[current_player] = f"{name}, score: {score}"
                    count += 1
                results.append(match)
                match_id += 1
            return results if results else no_results
        return no_results

    def get_rounds(self, tournament_id: int = None) -> list:
        no_result = [{'rounds': 'Nothing to report'}]
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
            return data if data else no_result
        return no_result

    def set_match_results(self, tournament_id: int, match_index: int,
                          scores: list):
        doc = self._db.read('tournament', **{'id': tournament_id})[0][0]
        doc_id = doc.doc_id
        last_round = f"Round {len(doc['rounds'])}"
        match_to_update = doc['rounds'][last_round]['matches'][match_index]
        count = 0
        for score in scores:
            match_to_update[count][1] = score
            count += 1

        doc['rounds'][last_round]['matches'][match_index] = match_to_update

        self._db.update('tournament', item_id=doc_id, **doc)

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

    @staticmethod
    def get_player_name(player_id):
        return Player({'id': player_id}).get_player_name()
