# -*- coding: utf-8 -*-

from controller.main_controller import MainController
from models.tournament import Tournament
from view.main_view import MainView


def main_ui():
    """ Main function. """
    # Create instances of the model and the controller
    view = MainView()
    model = Tournament()
    MainController(model=model, view=view)


if __name__ == '__main__':
    main_ui()
