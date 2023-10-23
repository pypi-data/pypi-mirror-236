from .player import Player


class Human(Player):
    def move(self, board):
        unparsed_move = input("Player " + self.disc + " - choose a move: ").strip()
        move = board.parse_move(unparsed_move)
        while move is None:
            unparsed_move = input("Not a valid move. Choose again: ").strip()
            move = board.parse_move(unparsed_move)
        return move
