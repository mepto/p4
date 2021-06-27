import sys
from datetime import date

import config
from models.tournament import Tournament


class MainController:
    """ Create a Controller class to connect the GUI and the model """

    def __init__(self, view: object, model: object):
        """ Controller initializer. """
        self._view = view
        self._model = model
        self._view.welcome()
        self.main_menu()

    def main_menu(self):
        self._view.main_menu()
        main_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 4)])
        self.main_menu_choice(main_choice)

    def tournament_menu(self):
        self._view.tournament_menu()
        tournament_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 8)])
        self.tournament_menu_choice(tournament_choice)

    def player_menu(self):
        self._view.player_menu()
        player_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 4)])
        self.player_menu_choice(player_choice)

    def report_menu(self):
        self._view.report_menu()
        report_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 5)])
        self.report_menu_choice(report_choice)

    def main_menu_choice(self, choice):
        if choice == 0:
            self._view.exit()
            sys.exit()
        elif choice == 1:
            self.tournament_menu()
        elif choice == 2:
            self.player_menu()
        elif choice == 3:
            self.report_menu()

    def tournament_menu_choice(self, choice):
        if choice == 0:
            self._view.exit()
            sys.exit()
        elif choice == 1:
            self.main_menu()
        elif choice == 2:
            # tournament creation
            self.add_tournament()
            self.tournament_menu()
        elif choice == 3:
            self.set_match_results()
            self.tournament_menu()
        elif choice == 4:
            # List tournament players (alpha)
            self.tournament_players_report(sort_order='alpha')
            self.tournament_menu()
        elif choice == 5:
            # List tournament players (ranking)
            self.tournament_players_report(sort_order='ranking')
            self.tournament_menu()
        elif choice == 6:
            # List tournament matches
            self.tournament_matches_report()
            self.tournament_menu()
        elif choice == 7:
            # List tournament rounds
            self.tournament_rounds_reports()
            self.tournament_menu()

    def player_menu_choice(self, choice):
        if choice == 0:
            self._view.exit()
            sys.exit()
        elif choice == 1:
            self.main_menu()
        elif choice == 2:
            # player creation
            self.add_player()
            self.player_menu()
        elif choice == 3:
            # player edition
            ...

    def report_menu_choice(self, choice):
        if choice == 0:
            self._view.exit()
            sys.exit()
        elif choice == 1:
            self.main_menu()
        elif choice == 2:
            # tournament print report
            self.tournament_report()
            self.report_menu()
        elif choice == 3:
            # player print report - alpha
            self.players_report()
            self.report_menu()
        elif choice == 4:
            # player print report - ranking
            self.players_report(sort_order='ranking')
            self.report_menu()

    def add_tournament(self):
        data = {}
        for item in config.NEW_TOURNAMENT:
            data[item] = self._view.get_user_input(config.NEW_TOURNAMENT[item])
        if not data['date']:
            data['date'] = date.today().strftime('%d/%m/%Y')
        data['players'] = []
        self._model = Tournament({})
        for i in range(0, self._model.nb_players):
            self._view.show_items(self._model.get_players())
            data['players'].append(int(self._view.get_user_input(config.SELECT_PLAYER)))
        self._model = Tournament(self._model.create_tournament(data))
        self._view.confirm('tournament')
        self._view.show_items(self._model.show_latest_pairs())
        self._view.confirm('pairs')

    def add_player(self):
        player = {}
        for item in config.NEW_PLAYER:
            player[item] = self._view.get_user_input(config.NEW_PLAYER[item])
        if not player['ranking']:
            player['ranking'] = 9999
        self._model = Tournament({})
        self._model.create_player(player)
        self._view.confirm('player')

    def set_match_results(self):
        # Get user to select tournament and match
        is_entering_score = True
        tournament_id = self.select_tournament()
        self._model = Tournament({'id': tournament_id})

        while is_entering_score:
            matches = self._model.get_matches(last_round=True)
            self._view.show_items(matches)
            match = self._view.get_user_choice(config.SELECT_MATCH, [*range(1, len(matches) + 1)]) - 1
            final_scores = []
            count = 1
            # Get user to enter new scores
            for item in config.SET_SCORES:
                player = f'Player {count}'
                final_scores.append(
                    float(self._view.get_user_input(f"{config.SET_SCORES[item]} ({matches[match][player]})")))
                count += 1
            # Manage new scores entry
            self._model.set_match_results(match, final_scores)
            # Check if round matches scores are full
            if self._model.is_round_over():
                self._model.set_round_end()
                self._model.create_new_round()
                self._model.show_latest_pairs()
            else:
                # Ask for new entry
                new_entry = int(self._view.get_user_choice(config.ADD_ANOTHER, [0, 1]))
                if not new_entry:
                    is_entering_score = False

    # Tournament reports
    def tournament_players_report(self, sort_order='alpha'):
        """Show players for a single tournament"""
        self._model = Tournament({'id': self.select_tournament()})
        self.players_report(sort_order)

    def select_tournament(self) -> int:
        # lists all tournaments and returns the selected id
        all_tournaments = self.tournament_report()
        ids = [item['id'] for item in all_tournaments]
        return self._view.get_user_choice(config.SELECT_TOURNAMENT, ids)

    def tournament_matches_report(self):
        """Show matches for a single tournament"""
        tournament_id = self.select_tournament()
        self._view.report(self._model.get_matches(tournament_id))

    def tournament_rounds_reports(self):
        """Show rounds for a single tournament"""
        tournament_id = self.select_tournament()
        self._view.report(self._model.get_rounds(tournament_id))

    # Full reports
    def players_report(self, sort_order='alpha'):
        """Show all players in DB"""
        self._view.report(self._model.get_players(sort_order))

    def tournament_report(self):
        """Show all tournaments in DB"""
        if not self._model:
            self._model = Tournament({})
        self._view.report(self._model.get_tournaments())
        return self._model.get_tournaments()
