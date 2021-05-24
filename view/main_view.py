# -*- coding: utf-8 -*-
from tabulate import tabulate

import config


class MainView:
    """ Display messages to the user in the console """
    @staticmethod
    def welcome():
        print(config.WELCOME)

    @staticmethod
    def main_menu():
        print(config.MAIN_MENU)

    @staticmethod
    def tournament_menu():
        print(config.TOURNAMENT_MENU)

    @staticmethod
    def player_menu():
        print(config.PLAYER_MENU)

    @staticmethod
    def report_menu():
        print(config.REPORT_MENU)

    @staticmethod
    def exit():
        print(config.EXIT)

    @staticmethod
    def get_user_choice(message: str, choice_list: list) -> int:
        """
        Loops until user enters proper choice
        :return: user choice
        """
        user_choice = input(message)
        while not user_choice or not user_choice.isdigit() or \
                int(user_choice) not in choice_list:
            reason = None
            if len(user_choice) == 0:
                reason = 'Empty entry.'
            elif not user_choice.isdigit():
                reason = f'"{user_choice}" is not a number'
            elif int(user_choice) not in choice_list:
                reason = f'Entry "{user_choice}" is not in available choices.'

            user_choice = input(f'{reason}\n{message}')

        return int(user_choice)

    @staticmethod
    def get_user_input(message):
        return input(f'{message}: ')

    @staticmethod
    def show_items(items: list):
        all_items = [dict(doc) for doc in items]
        header = {key: key.upper() for data in all_items for key in data.keys()}
        print(tabulate(all_items, header, tablefmt="github"))

    def report(self, doc_list: list):
        self.show_items(doc_list)
        print(config.REPORT_END)

    def confirm(self, item: str):
        print(f"*** {item.capitalize()} created successfully ***")
