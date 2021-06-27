from datetime import datetime


class Round:
    def __init__(self, round_nb: int, matches: list):
        self.round_nb = f'Round {round_nb}'
        self.matches = matches
        self.start_time = self.get_now()
        self.end_time = None

    def set_end_time(self):
        self.end_time = self.get_now()

    @staticmethod
    def get_now():
        return datetime.now().isoformat()

    def serialize(self):
        return {
            self.round_nb: {
                'start_time': self.start_time,
                'end_time': self.end_time,
                'matches': self.matches
            }
        }
