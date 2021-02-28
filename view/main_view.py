# -*- coding: utf-8 -*-


class MainView:

    DEFAULT_MSG = 'Please make your selection: '
    NEW_TOURNAMENT = {'name': 'Enter tournament name',
                      'location': 'Enter tournament location',
                      'date': 'Enter tournament date (dd/mm/yyyy)'}

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
        ---------------------
        3 - Create player
        4 - Edit player
        ---------------------
        5 - View report
        6 - Export report
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
