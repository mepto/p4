# -*- coding: utf-8 -*-


class MainView:

    def welcome(self):
        print("********************************************")
        print("* Welcome to your chess tournament manager *")
        print("********************************************")

    def main_menu(self):
        print("---------------- MAIN MENU -----------------")
        print("1 - Create tournament")
        print("2 - Edit Tournament")

    def get_user_choice(self, message, ):
        """
        Loops until user enters proper choice
        :return: user choice
        """
        user_choice = input(message)
        while not user_choice:
            user_choice = input(f'Incorrect entry "{user_choice}". {message}')

        return user_choice
