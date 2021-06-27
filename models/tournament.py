from datetime import datetime

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
            self.location = existing_tournament['location'] or tournament['location']
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
        self.players = data['players']
        self.rounds = Round(1, self.generate_pairs()).serialize()
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
            for player in all_players:
                if player['id'] not in self.players:
                    all_players.remove(player)
        if order == 'alpha':
            all_players.sort(key=lambda item: item.get('last_name').upper())
        elif order == 'ranking':
            all_players.sort(key=lambda item: item.get('ranking'))
        return all_players

    def get_matches(self, last_round: bool = False) -> list:
        no_results = [{'matches': 'Nothing to report'}]
        if self.id:
            tournament_data = self._db.read('tournament', **{'id': self.id})[0][0]
            rounds = tournament_data['rounds']
            matches = []
            results = []
            if last_round:
                current_round = next(reversed(rounds.keys()))
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
        self.rounds = doc['rounds']
        self._db.update('tournament', item_id=doc_id, **doc)

    def is_round_over(self):
        doc = self._db.read('tournament', **{'id': self.id})[0][0]
        last_round = f"Round {len(doc['rounds'])}"
        for item in doc['rounds'][last_round]['matches']:
            if None in [item[0][1], item[1][1]]:
                return False
        return True

    def set_round_end(self):
        doc = self._db.read('tournament', **{'id': self.id})[0][0]
        doc_id = doc.doc_id
        last_round = f"Round {len(doc['rounds'])}"
        doc['rounds'][last_round]['end_time'] = datetime.now().isoformat()
        self._db.update('tournament', item_id=doc_id, **doc)

    def create_new_round(self):
        doc = self._db.read('tournament', **{'id': self.id})[0][0]
        doc_id = doc.doc_id
        all_rounds = doc['rounds']
        len_rounds = len(all_rounds)
        # self.generate_pairs()
        new_round = Round(len_rounds + 1, self.generate_pairs()).serialize()
        doc['rounds'].update(new_round)
        self.rounds = doc['rounds']
        self._db.update('tournament', item_id=doc_id, **doc)

    def generate_pairs(self) -> list:
        if not self.rounds:
            return self.pair_by_ranking()
        else:
            return self.pair_by_points()

    def show_latest_pairs(self) -> list:
        pairs = []
        latest_round = list(self.rounds.keys())[-1]
        for item in self.rounds[latest_round]['matches']:
            pairs.append({
                'player_1': Player({'id': item[0][0]}).get_player_name(),
                'player_2': Player({'id': item[1][0]}).get_player_name()
            })
        return pairs

    def pair_by_ranking(self) -> list:
        players_list = []
        # retrieve players and sort rankings
        for p in self.players:
            players_list.append(Player().get_rank(p))
        players_list.sort(key=lambda player: player[1])
        half = int(len(players_list) / 2)
        match_list = []
        for p in players_list[:(half)]:
            second_player_index = players_list.index(p) + half
            match = Match(p[0], players_list[second_player_index][0])
            match_list.append(match.serialize())
        return match_list

    def pair_by_points(self):
        match_list = []
        initial_scoreboard = self.create_scoreboard()
        scoreboard = initial_scoreboard.copy()
        match_nb = 1
        while match_nb <= (len(self.players) / 2):
            current_player = next(iter(scoreboard.items()))
            current_opponent = current_player[1]['playables'][0]
            match = Match(current_player[0], current_opponent)
            match_list.append(match.serialize())
            for item in scoreboard:
                try:
                    scoreboard[item]['playables'].remove(current_opponent)
                except ValueError:
                    pass
                try:
                    scoreboard[item]['playables'].remove(current_player[0])
                except ValueError:
                    pass
            scoreboard.pop(current_player[0])
            scoreboard.pop(current_opponent)
            match_nb += 1

        return match_list

    def create_scoreboard(self):
        scoreboard = {}
        all_matches = []
        for item in self.rounds:
            for match in self.rounds[item]['matches']:
                all_matches.append([match[0][0], match[1][0]])
                for player in match:
                    player_id = player[0]
                    player_score = player[1]
                    if player_id not in scoreboard:
                        scoreboard[player_id] = {
                            'score': player_score}
                    else:
                        scoreboard[player_id]['score'] = (scoreboard[player_id]['score'] + player_score)

        ordered_players = sorted(scoreboard, key=lambda item: (scoreboard[item]['score']), reverse=True)
        sorted_scoreboard = {}
        for item in ordered_players:
            sorted_scoreboard[item] = scoreboard[item]

        for player in sorted_scoreboard:
            sorted_scoreboard[player]['playables'] = ordered_players.copy()
            player_index = scoreboard[player]['playables'].index(player)
            sorted_scoreboard[player]['playables'].pop(player_index)
            for match in all_matches:
                if player in match:
                    player_index = match.index(player)
                    opponent = match[player_index + 1] if player_index == 0 else match[player_index - 1]
                    opponent_index = scoreboard[player]['playables'].index(opponent)
                    scoreboard[player]['playables'].pop(opponent_index)

        return sorted_scoreboard

    @staticmethod
    def get_player_name(player_id):
        return Player({'id': player_id}).get_player_name()
