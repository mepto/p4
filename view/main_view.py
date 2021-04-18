# -*- coding: utf-8 -*-
from tabulate import tabulate


class MainView:
    DEFAULT_MSG = 'Please make your selection: '
    NEW_TOURNAMENT = {'name': 'Enter tournament name',
                      'location': 'Enter tournament location',
                      'date': 'Enter tournament date (dd/mm/yyyy)',
                      'time_control': 'Enter time control type (bullet, '
                                      'blitz, speed)'}
    NEW_PLAYER = {'last_name': "Enter player's last name",
                  'first_name': "Enter player's first name",
                  'dob': "Enter player's date of birth (dd/mm/yyyy)",
                  'gender': "Enter player's gender (M/F/O)",
                  'ranking': "Enter player's ranking"}
    SELECT_PLAYER = 'Please select a player'

    @staticmethod
    def welcome():
        print('''
        ********************************************
        * Welcome to your chess tournament manager *
        ********************************************
        ''')

    @staticmethod
    def main_menu():
        print('''
        ---------------- MAIN MENU -----------------
        0 - Exit
        ---------------------
        1 - Tournament management
        2 - Player management
        3 - Global reports
        ''')

    @staticmethod
    def tournament_menu():
        print('''
        ------------- TOURNAMENT MENU --------------
        0 - Exit
        1 - Back
        ---------------------
        2 - Create tournament
        3 - Enter match results
        4 - List tournament players (alpha)
        5 - List tournament players (ranking)
        6 - List tournament matches
        7 - List tournament rounds
        ''')

    @staticmethod
    def player_menu():
        print('''
        --------------- PLAYER MENU ----------------
        0 - Exit
        1 - Back
        ---------------------
        2 - Create player
        3 - Edit player
        ''')

    @staticmethod
    def report_menu():
        print('''
        --------------- REPORT MENU ----------------
        0 - Exit
        1 - Back
        ---------------------
        2 - All tournaments report
        3 - All players report (alpha)
        4 - All players report (ranking)
        ''')

    @staticmethod
    def exit():
        print("--------------- SEE YOU SOON ----------------")

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
        print('--------------- END OF REPORT ---------------')

    def confirm(self, item: str):
        print(f"*** {item.capitalize()} created successfully ***")
