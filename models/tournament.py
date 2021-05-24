# -*- coding: utf-8 -*-

from helpers.database import Database
from helpers.match import Match
from helpers.round import Round
from models.player import Player


class Tournament:
    """Manage a tournament"""

    def __init__(self, tournament: dict = {}):
        self._db = Database()
        self.nb_players = 8
        if tournament and 'id' in tournament:
            self.id = tournament['id']
            existing_tournament = self.get_tournament(self.id)[0][0]
            self.players = existing_tournament['players'] or []
            self.matches = []
            self.rounds = existing_tournament['rounds'] or {}
            self.time_control = existing_tournament['time_control'] or 'bullet'
            self.description = existing_tournament['description'] or None
            self.name = existing_tournament['name'] or None
            self.location = existing_tournament['location'] or tournament[
                'location']
            self.date = existing_tournament['date'] or tournament['date']
        else:
            self.id = None
            self.players = []
            self.matches = []
            self.rounds = {}
            self.time_control = 'bullet'
            self.description = None
            self.name = None
            self.location = None
            self.date = None

    def get_next_id(self, table: str = 'tournament') -> int:
        return self._db.get_next_id(table)

    def create_tournament(self, tournament: dict):
        new_id = self._db.get_next_id('tournament')
        data = {'id': new_id}
        for key, value in tournament.items():
            data[key] = value
        if 'time_control' not in data or not data['time_control']:
            data['time_control'] = self.time_control
        self.rounds = Round(1,
                            self.generate_pairs(data['players'])).serialize()
        data['rounds'] = self.rounds
        self._db.create('tournament', data)
        return {'id': new_id}

    @staticmethod
    def create_player(player: dict):
        Player(player).create()

    def get_tournaments(self) -> list:
        return self._db.read('tournament')

    def get_tournament(self, tournament_id) -> list:
        return self._db.read('tournament', **{'id': tournament_id})

    def get_players(self, order: str = None) -> list:
        all_players = Player().get_players()  # list of dicts
        if self.id:
            tournament = self._db.read('tournament', **{'id': self.id})
            for player in all_players:
                if player['id'] not in tournament[0]['players']:
                    all_players.remove(player)
        if order == 'alpha':
            all_players.sort(key=lambda item: item.get('last_name').upper())
        elif order == 'ranking':
            all_players.sort(key=lambda item: item.get('ranking'))
        return all_players

    def get_matches(self, last_round: bool = False) -> list:
        no_results = [{'matches': 'Nothing to report'}]
        if self.id:
            tournament_data = self._db.read('tournament',
                                            **{'id': self.id})[0][0]
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

    def get_rounds(self) -> list:
        no_result = [{'rounds': 'Nothing to report'}]
        if self.id:
            data = []
            db_data = self._db.read('tournament', **{'id': self.id})
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

    def set_match_results(self, match_index: int, scores: list):
        doc = self._db.read('tournament', **{'id': self.id})[0][0]
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
