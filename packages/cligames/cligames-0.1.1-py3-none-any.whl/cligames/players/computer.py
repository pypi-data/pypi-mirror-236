import math
import collections
from .player import Player


class Computer(Player):
    def move(self, board):
        print("Player " + self.disc + " is choosing...", end=" ", flush=True)
        move = self.minimax(board, 0, 6, -math.inf, math.inf)
        print("")
        return move

    def minimax(self, board, current_depth, max_depth, alpha, beta):
        board_score = 0
        level = collections.deque([])
        if (
            (current_depth == max_depth)
            or (board.board_full() == True)
            or board.check_for_win(self.disc)
            or board.check_for_win(self.opponent_disc)
        ):
            board_score += board.player_score(
                1, 100, 100000, self.disc
            )  # player evaluation (positive)
            board_score -= board.player_score(
                10, 1000, 1000000, self.opponent_disc
            )  # opponent evaluation (negative)
            return board_score
        if current_depth == 0:
            for move in board.moves:
                if board.place_disc(self.disc, move, "simulation") != "full":
                    current_val = self.minimax(
                        board, current_depth + 1, max_depth, alpha, beta
                    )
                    level.append(current_val)
                    board.remove_disc(self.disc, move)
                    alpha = max(alpha, current_val)
                else:
                    level.append(-math.inf)
            chosen_move = board.moves[level.index(max(level))]
            return chosen_move
        elif current_depth % 2 == 0:
            best_val = -math.inf
            for move in board.moves:
                if board.place_disc(self.disc, move, "simulation") != "full":
                    current_val = self.minimax(
                        board, current_depth + 1, max_depth, alpha, beta
                    )
                    best_val = max(best_val, current_val)
                    board.remove_disc(self.disc, move)
                    alpha = max(alpha, current_val)
                    if alpha >= beta:
                        break
            return best_val
        else:
            best_val = math.inf
            for move in board.moves:
                if board.place_disc(self.opponent_disc, move, "simulation") != "full":
                    current_val = self.minimax(
                        board, current_depth + 1, max_depth, alpha, beta
                    )
                    best_val = min(best_val, current_val)
                    board.remove_disc(self.opponent_disc, move)
                    beta = min(beta, current_val)
                    if alpha >= beta:
                        break
            return best_val
