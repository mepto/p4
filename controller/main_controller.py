# -*- coding: utf-8 -*-
import sys
from datetime import date


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
        main_choice = self._view.get_user_choice(self._view.DEFAULT_MSG,
                                                 [*range(0, 4)])
        self.main_menu_choice(main_choice)

    def tournament_menu(self):
        self._view.tournament_menu()
        tournament_choice = self._view.get_user_choice(self._view.DEFAULT_MSG,
                                                       [*range(0, 8)])
        self.tournament_menu_choice(tournament_choice)

    def player_menu(self):
        self._view.player_menu()
        player_choice = self._view.get_user_choice(self._view.DEFAULT_MSG,
                                                   [*range(0, 4)])
        self.player_menu_choice(player_choice)

    def report_menu(self):
        self._view.report_menu()
        report_choice = self._view.get_user_choice(self._view.DEFAULT_MSG,
                                                   [*range(0, 5)])
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
            self.enter_match_results()
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
            ...

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
        tournament = {}
        for item in self._view.NEW_TOURNAMENT:
            tournament[item] = self._view.get_user_input(
                self._view.NEW_TOURNAMENT[item])
        if not tournament['date']:
            tournament['date'] = date.today().strftime('%d/%m/%Y')
        tournament['players'] = []
        for i in range(0, self._model.nb_players):
            self._view.show_items(self._model.get_players())
            tournament['players'].append(int(self._view.get_user_input(
                self._view.SELECT_PLAYER)))
        self._model.create_tournament(tournament)
        self._view.confirm('tournament')
        self._view.confirm('pairs')
        self._view.show_items(self._model.show_latest_pairs())

    def add_player(self):
        player = {}
        for item in self._view.NEW_PLAYER:
            player[item] = self._view.get_user_input(
                self._view.NEW_PLAYER[item])
        if not player['ranking']:
            player['ranking'] = 9999
        self._model.create_player(player)
        self._view.confirm('player')

    def enter_match_results(self):
        self._view.enter_match_results()

    # Tournament reports
    def tournament_players_report(self, sort_order='alpha'):
        """Show players for a single tournament"""
        # get user to select tournament
        tournament_id = self.select_tournament()
        self.players_report(tournament_id, sort_order)

    def select_tournament(self):
        # lists all tournaments and returns the selected id
        all_tournaments = self.tournament_report()
        return self._view.get_user_choice(
            'Select a tournament', [*range(1, len(all_tournaments) + 1)])

    def tournament_matches_report(self):
        """Show matches for a single tournament"""
        tournament_id = self.select_tournament()
        self._view.report(self._model.get_matches(tournament_id))

    def tournament_rounds_reports(self):
        """Show rounds for a single tournament"""
        tournament_id = self.select_tournament()
        self._view.report(self._model.get_rounds(tournament_id))

    # Full reports
    def players_report(self, tournament_id=None, sort_order='alpha'):
        """Show all players in DB"""
        self._view.report(self._model.get_players(tournament_id, sort_order))

    def tournament_report(self):
        """Show all tournaments in DB"""
        self._view.report(self._model.get_tournaments())
        return self._model.get_tournaments()
