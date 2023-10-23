from .board import Board


class Tictactoe(Board):
    def __init__(self):
        self.num_rows = 3
        self.num_columns = 3
        self.b = [
            [" " for row in range(self.num_rows)] for column in range(self.num_columns)
        ]
        self.moves = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
        ]
        self.disc_1 = "X"
        self.disc_2 = "O"

    def print_board(self):
        print(
            "  |---|---|---|\n"
            "2 | "
            + self.b[0][2]
            + " | "
            + self.b[1][2]
            + " | "
            + self.b[2][2]
            + " | \n"
            "  |---|---|---|\n"
            "1 | "
            + self.b[0][1]
            + " | "
            + self.b[1][1]
            + " | "
            + self.b[2][1]
            + " | \n"
            "  |---|---|---|\n"
            "0 | "
            + self.b[0][0]
            + " | "
            + self.b[1][0]
            + " | "
            + self.b[2][0]
            + " | \n"
            "  |---|---|---|\n"
            "    0   1   2 \n"
        )

    def parse_move(self, unparsed_move):
        try:
            if unparsed_move.strip()[0] != "(" or unparsed_move.strip()[-1] != ")":
                return None
            player_move = tuple(
                [int(val.strip()) for val in unparsed_move.strip()[1:-1].split(",")]
            )
            for move in self.moves:
                if player_move == move:
                    return player_move
            return None
        except ValueError:
            return None

    def board_full(self):
        for i in range(0, self.num_columns):
            for j in range(0, self.num_rows):
                if self.b[i][j] == " ":
                    return False
        return True

    def reset_board(self):
        for i in range(0, self.num_columns):
            for j in range(0, self.num_rows):
                self.b[i][j] = " "

    def place_disc(self, disc, position, situation):
        pos_x, pos_y = position
        if self.b[pos_x][pos_y] == " ":
            self.b[pos_x][pos_y] = disc
            return
        if situation == "game":
            unparsed_move = input(
                "This position is taken. Please choose a different one: "
            ).strip()
            move = self.parse_move(unparsed_move)
            while move is None:
                unparsed_move = input("Not a valid move. Choose again: ").strip()
                move = self.parse_move(unparsed_move)
            self.place_disc(disc, move, "game")
        else:
            return "full"

    def remove_disc(self, disc, position):
        pos_x, pos_y = position
        if self.b[pos_x][pos_y] == disc:
            self.b[pos_x][pos_y] = " "
            return

    def state_scanner(self, disc1, disc2, disc3):
        score = 0
        # east scan
        for j in range(0, self.num_rows):
            if (
                (self.b[0][j] == disc1)
                and (self.b[1][j] == disc2)
                and (self.b[2][j] == disc3)
            ):
                score += 1
        # north scan
        for i in range(0, self.num_columns):
            if (
                (self.b[i][0] == disc1)
                and (self.b[i][1] == disc2)
                and (self.b[i][2] == disc3)
            ):
                score += 1
        # north east scan
        if (
            (self.b[0][0] == disc1)
            and (self.b[1][1] == disc2)
            and (self.b[2][2] == disc3)
        ):
            score += 1
        # north east reverse scan
        if (
            (self.b[0][2] == disc1)
            and (self.b[1][1] == disc2)
            and (self.b[2][0] == disc3)
        ):
            score += 1
        return score

    def player_score(self, one_score, two_score, three_score, disc):
        player_score = 0
        player_score += one_score * self.state_scanner(disc, " ", " ")
        player_score += one_score * self.state_scanner(" ", disc, " ")
        player_score += one_score * self.state_scanner(" ", " ", disc)
        player_score += two_score * self.state_scanner(disc, disc, " ")
        player_score += two_score * self.state_scanner(disc, " ", disc)
        player_score += two_score * self.state_scanner(" ", disc, disc)
        player_score += three_score * self.state_scanner(disc, disc, disc)
        return player_score

    def check_for_win(self, player_disc):
        if self.state_scanner(player_disc, player_disc, player_disc) > 0:
            return True
        else:
            return False
