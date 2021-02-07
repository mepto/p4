# -*- coding: utf-8 -*-


class MainController:
    """ Create a Controller class to connect the GUI and the model """

    def __init__(self, view: object, model: object):
        """ Controller initializer. """
        self._view = view
        self._model = model
        self.start()

    def start(self):
        self._view.welcome()
        self._view.main_menu()
