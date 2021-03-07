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
                                                 [*range(0, 7)])
        self.main_menu_choice(main_choice)

    def main_menu_choice(self, choice):
        if choice == 0:
            self._view.exit()
            sys.exit()
        elif choice == 1:
            # tournament creation
            self.add_tournament()
        elif choice == 2:
            # tournament edition
            ...
        elif choice == 3:
            # tournament print report
            self.tournament_report()
            ...
        elif choice == 4:
            # player creation
            self.add_player()
            ...
        elif choice == 5:
            # player edition
            ...
        elif choice == 6:
            # player print report
            self.players_report()

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

    def add_player(self):
        player = {}
        for item in self._view.NEW_PLAYER:
            player[item] = self._view.get_user_input(
                self._view.NEW_PLAYER[item])
        if not player['ranking']:
            player['ranking'] = 9999
        self._model.create_player(player)

    def players_report(self):
        self._view.report(self._model.get_players())
        self.main_menu()

    def tournament_report(self):
        self._view.report(self._model.get_tournaments())
        self.main_menu()
