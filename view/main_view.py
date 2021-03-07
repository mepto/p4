# -*- coding: utf-8 -*-
import pandas as pd


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
    SELECT_PLAYER = 'Select player from players list'

    def welcome(self):
        print('''
        ********************************************
        * Welcome to your chess tournament manager *
        ********************************************
        ''')

    def main_menu(self):
        print('''
        ---------------- MAIN MENU -----------------
        0 - Exit
        ---------------------
        1 - Create tournament
        2 - Edit tournament
        3 - View tournament report
        ---------------------
        4 - Create player
        5 - Edit player
        6 - View player report
        ''')

    def exit(self):
        print("---------------- THANK YOU! -----------------")

    def get_user_choice(self, message, choice_list):
        """
        Loops until user enters proper choice
        :return: user choice
        """
        user_choice = input(message)
        while not user_choice or not user_choice.isdigit() or\
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

    def get_user_input(self, message):
        return input(f'{message}: ')

    def show_items(self, doc_list: list):
        all_items = [dict(doc) for doc in doc_list]
        df = pd.DataFrame(all_items)
        print(df.to_string(index=False))

    def report(self, doc_list: list):
        self.show_items(doc_list)
        print('--------------- END OF REPORT ---------------')
