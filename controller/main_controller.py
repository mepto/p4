import sys
from datetime import date

import config
from models.tournament import Tournament


class MainController:
    """ Create a Controller class to connect the GUI and the model """

    def __init__(self, view: object, model: object):
        """ Controller initializer """
        self._view = view
        self._model = model

        self.MAIN_MENU = {
            0: self.exit_application,
            1: self.tournament_menu,
            2: self.player_menu
        }

        self.TOURNAMENT_MENU = {
            0: self.exit_application,
            1: self.main_menu,
            2: self.add_tournament,
            3: self.set_match_results,
            4: self.tournament_players_report_alpha,
            5: self.tournament_players_report_ranking,
            6: self.tournament_matches_report,
            7: self.tournament_rounds_reports,
            8: self.tournament_report
        }

        self.PLAYER_MENU = {
            0: self.exit_application,
            1: self.main_menu,
            2: self.add_player,
            3: self.edit_player,
            4: self.players_report_alpha,
            5: self.players_report_ranking
        }

        self._view.welcome()
        self.main_menu()

    def main_menu(self):
        self._view.main_menu()
        main_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 3)])
        self.MAIN_MENU.get(main_choice)()

    def tournament_menu(self):
        self._view.tournament_menu()
        tournament_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 9)])
        self.TOURNAMENT_MENU.get(tournament_choice)()

    def player_menu(self):
        self._view.player_menu()
        player_choice = self._view.get_user_choice(config.DEFAULT_MSG, [*range(0, 6)])
        self.PLAYER_MENU.get(player_choice)()

    def exit_application(self):
        self._view.exit()
        sys.exit()

    def add_tournament(self):
        data = {}
        for item in config.NEW_TOURNAMENT:
            data[item] = self._view.get_user_input(config.NEW_TOURNAMENT[item])
        if not data['date']:
            data['date'] = date.today().strftime('%d/%m/%Y')
        data['players'] = []
        self._model = Tournament({})
        for i in range(0, self._model.nb_players):
            self._view.show_items(self._model.get_players())
            data['players'].append(int(self._view.get_user_input(config.SELECT_PLAYER)))
        self._model = Tournament(self._model.create_tournament(data))
        self._view.confirm('tournament')
        self._view.show_items(self._model.show_latest_pairs())
        self._view.confirm('pairs')
        self.tournament_menu()

    def add_player(self):
        player = {}
        for item in config.NEW_PLAYER:
            player[item] = self._view.get_user_input(config.NEW_PLAYER[item])
        if not player['ranking']:
            player['ranking'] = 9999
        self._model = Tournament({})
        self._model.create_player(player)
        self._view.confirm('player')

        self.player_menu()

    def edit_player(self):
        self._model = Tournament({})
        all_players = self._model.get_players()
        self._view.show_items(all_players)
        ids = [item['id'] for item in all_players]
        player = self._view.get_user_choice(config.SELECT_PLAYER, ids)
        player_data = self._model.get_player(player)
        new_player_data = {}
        for item in config.NEW_PLAYER:
            if item == 'ranking':
                new_data = int(self._view.get_user_input(
                    f'{config.NEW_PLAYER[item]} (current data: {player_data[item]}, press enter to keep as is)'))
            else:
                new_data = self._view.get_user_input(f'{config.NEW_PLAYER[item]} (current data: {player_data[item]}, '
                                                     f'press enter to keep as is)')
            if new_data:
                new_player_data[item] = new_data
            else:
                new_player_data[item] = player_data[item]
        new_player_data['id'] = player_data['id']
        self._model.edit_player(new_player_data)
        self._view.confirm('player')

        self.player_menu()

    def set_match_results(self):
        # Get user to select tournament and match
        is_entering_score = True
        tournament_id = self.select_tournament()
        self._model = Tournament({'id': tournament_id})

        while is_entering_score:
            matches = self._model.get_matches(last_round=True)
            self._view.show_items(matches)
            match = self._view.get_user_choice(config.SELECT_MATCH, [*range(1, len(matches) + 1)]) - 1
            final_scores = []
            count = 1
            # Get user to enter new scores
            for item in config.SET_SCORES:
                player = f'Player {count}'
                final_scores.append(
                    float(self._view.get_user_input(f"{config.SET_SCORES[item]} ({matches[match][player]})")))
                count += 1
            # Manage new scores entry
            self._model.set_match_results(match, final_scores)
            # Check if round matches scores are full
            if self._model.is_round_over():
                self._model.set_round_end()
                if len(self._model.rounds) < len(self._model.players) / 2:
                    self._model.create_new_round()
                    self._model.show_latest_pairs()
                else:
                    self._view.rounds_done()
                    is_entering_score = False
            else:
                # Ask for new entry
                new_entry = int(self._view.get_user_choice(config.ADD_ANOTHER, [0, 1]))
                if not new_entry:
                    is_entering_score = False
        self.tournament_menu()

    # Tournament reports

    def tournament_players_report_alpha(self):
        self.tournament_players_report()

    def tournament_players_report_ranking(self):
        self.tournament_players_report('ranking')

    def tournament_players_report(self, sort_order='alpha'):
        """Show players for a single tournament"""
        self._model = Tournament({'id': self.select_tournament()})
        self.players_report(sort_order)

        self.tournament_menu()

    def select_tournament(self) -> int:
        # lists all tournaments and returns the selected id
        all_tournaments = self.tournament_report(needs_selection=True)
        ids = [item['id'] for item in all_tournaments]
        return self._view.get_user_choice(config.SELECT_TOURNAMENT, ids)

    def tournament_matches_report(self):
        """Show matches for a single tournament"""
        tournament_id = self.select_tournament()
        self._model = Tournament({'id': tournament_id})
        self._view.report(self._model.get_matches())

        self.tournament_menu()

    def tournament_rounds_reports(self):
        """Show rounds for a single tournament"""
        tournament_id = self.select_tournament()
        self._model = Tournament({'id': tournament_id})
        self._view.report(self._model.get_rounds())

        self.tournament_menu()

    # Full reports
    def players_report_alpha(self):
        self.players_report()
        self.player_menu()

    def players_report_ranking(self):
        self.players_report('ranking')
        self.player_menu()

    def players_report(self, sort_order='alpha'):
        """Show all players in DB"""
        self._view.report(self._model.get_players(sort_order))

    def tournament_report(self, needs_selection=False):
        """Show all tournaments in DB"""
        if not self._model:
            self._model = Tournament({})
        self._view.report(self._model.get_tournaments())
        if needs_selection:
            return self._model.get_tournaments()
        else:
            self.tournament_menu()
