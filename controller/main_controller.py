# -*- coding: utf-8 -*-
import sys
from datetime import date


class MainController:
    """ Create a Controller class to connect the GUI and the model """

    def __init__(self, view: object, model: object):
        """ Controller initializer. """
        self._view = view
        self._model = model

        self.main_menu()

    def main_menu(self):
        self._view.welcome()
        self._view.main_menu()
        main_choice = self._view.get_user_choice(self._view.DEFAULT_MSG,
                                                 [*range(0, 6)])
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
            # player creation
            ...
        elif choice == 4:
            # player edition
            ...
        elif choice == 5:
            # reporting in view
            ...
        elif choice == 6:
            # reporting file export
            ...

    def add_tournament(self):
        tournament = {}
        for item in self._view.NEW_TOURNAMENT:
            tournament[item] = self._view.get_user_input(
                self._view.NEW_TOURNAMENT[item])
        if not tournament['date']:
            tournament['date'] = date.today().strftime('%d/%m/%Y')
        self._model.create_tournament(tournament)
