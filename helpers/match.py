class Match:
    def __init__(self, player_1: int, player_2: int, score_p1=None,
                 score_p2=None):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_p1 = score_p1
        self.score_p2 = score_p2

    def serialize(self) -> tuple:
        return ([self.player_1, self.score_p1], [self.player_2, self.score_p2])

    def set_score(self, score_p1: float, score_p2: float) -> dict:
        self.score_p1 = score_p1
        self.score_p2 = score_p2
        return self.serialize()
