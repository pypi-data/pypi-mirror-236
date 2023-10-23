class Player:
    def __init__(self, disc, opponent_disc):
        self.disc = disc
        self.opponent_disc = opponent_disc

    def move(self, board):
        raise NotImplementedError
