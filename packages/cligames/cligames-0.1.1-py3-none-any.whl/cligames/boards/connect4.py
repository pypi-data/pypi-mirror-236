from .board import Board


class Connect4(Board):
    def __init__(self):
        self.num_rows = 6
        self.num_columns = 7
        self.b = [
            [" " for row in range(self.num_rows)] for column in range(self.num_columns)
        ]
        self.moves = [0, 1, 2, 3, 4, 5, 6]
        self.disc_1 = "X"
        self.disc_2 = "O"

    def print_board(self):
        print(
            "|---|---|---|---|---|---|---|\n"
            "| "
            + self.b[0][5]
            + " | "
            + self.b[1][5]
            + " | "
            + self.b[2][5]
            + " | "
            + self.b[3][5]
            + " | "
            + self.b[4][5]
            + " | "
            + self.b[5][5]
            + " | "
            + self.b[6][5]
            + " |\n"
            "|---|---|---|---|---|---|---|\n"
            "| "
            + self.b[0][4]
            + " | "
            + self.b[1][4]
            + " | "
            + self.b[2][4]
            + " | "
            + self.b[3][4]
            + " | "
            + self.b[4][4]
            + " | "
            + self.b[5][4]
            + " | "
            + self.b[6][4]
            + " |\n"
            "|---|---|---|---|---|---|---|\n"
            "| "
            + self.b[0][3]
            + " | "
            + self.b[1][3]
            + " | "
            + self.b[2][3]
            + " | "
            + self.b[3][3]
            + " | "
            + self.b[4][3]
            + " | "
            + self.b[5][3]
            + " | "
            + self.b[6][3]
            + " |\n"
            "|---|---|---|---|---|---|---|\n"
            "| "
            + self.b[0][2]
            + " | "
            + self.b[1][2]
            + " | "
            + self.b[2][2]
            + " | "
            + self.b[3][2]
            + " | "
            + self.b[4][2]
            + " | "
            + self.b[5][2]
            + " | "
            + self.b[6][2]
            + " |\n"
            "|---|---|---|---|---|---|---|\n"
            "| "
            + self.b[0][1]
            + " | "
            + self.b[1][1]
            + " | "
            + self.b[2][1]
            + " | "
            + self.b[3][1]
            + " | "
            + self.b[4][1]
            + " | "
            + self.b[5][1]
            + " | "
            + self.b[6][1]
            + " |\n"
            "|---|---|---|---|---|---|---|\n"
            "| "
            + self.b[0][0]
            + " | "
            + self.b[1][0]
            + " | "
            + self.b[2][0]
            + " | "
            + self.b[3][0]
            + " | "
            + self.b[4][0]
            + " | "
            + self.b[5][0]
            + " | "
            + self.b[6][0]
            + " |\n"
            "|---|---|---|---|---|---|---|\n"
            "  0   1   2   3   4   5   6  \n"
        )

    def parse_move(self, unparsed_move):
        try:
            player_move = int(unparsed_move.strip())
            for move in self.moves:
                if player_move == move:
                    return player_move
            return None
        except ValueError:
            return None

    def board_full(self):
        for i in range(0, self.num_columns):
            if self.b[i][len(self.b[0]) - 1] == " ":
                return False
        return True

    def reset_board(self):
        for i in range(0, self.num_columns):
            for j in range(0, self.num_rows):
                self.b[i][j] = " "

    def place_disc(self, disc, column, situation):
        for i in range(0, self.num_rows):
            if self.b[column][i] == " ":
                self.b[column][i] = disc
                return
        if situation == "game":
            unparsed_move = input(
                "This column is full. Please choose a different one: "
            ).strip()
            move = self.parse_move(unparsed_move)
            while move is None:
                unparsed_move = input("Not a valid move. Choose again: ").strip()
                move = self.parse_move(unparsed_move)
            self.place_disc(disc, move, "game")
        else:
            return "full"

    def remove_disc(self, disc, column):
        # loops backwards from top of column down to bottom
        for i in range(self.num_rows - 1, -1, -1):
            if self.b[column][i] == disc:
                self.b[column][i] = " "
                return

    def state_scanner(self, disc1, disc2, disc3, disc4):
        score = 0
        # east scan
        for i in range(0, self.num_columns - 3):  # [0 - 3]
            for j in range(0, self.num_rows):  # [0 - 5]
                if (
                    (self.b[i][j] == disc1)
                    and (self.b[i + 1][j] == disc2)
                    and (self.b[i + 2][j] == disc3)
                    and (self.b[i + 3][j] == disc4)
                ):
                    score += 1
        # north scan
        for i in range(0, self.num_columns):
            for j in range(0, self.num_rows - 3):
                if (
                    (self.b[i][j] == disc1)
                    and (self.b[i][j + 1] == disc2)
                    and (self.b[i][j + 2] == disc3)
                    and (self.b[i][j + 3] == disc4)
                ):
                    score += 1
        # north east scan
        for i in range(0, self.num_columns - 3):
            for j in range(0, self.num_rows - 3):
                if (
                    (self.b[i][j] == disc1)
                    and (self.b[i + 1][j + 1] == disc2)
                    and (self.b[i + 2][j + 2] == disc3)
                    and (self.b[i + 3][j + 3] == disc4)
                ):
                    score += 1
        # north east reverse scan
        for i in range(0, self.num_columns - 3):
            for j in range(0, self.num_rows - 3):
                if (
                    (self.b[i + 3][j] == disc1)
                    and (self.b[i + 2][j + 1] == disc2)
                    and (self.b[i + 1][j + 2] == disc3)
                    and (self.b[i][j + 3] == disc4)
                ):
                    score += 1
        return score

    def player_score(self, two_score, three_score, four_score, disc):
        player_score = 0
        player_score += self.state_scanner(disc, " ", " ", " ")
        player_score += self.state_scanner(" ", disc, " ", " ")
        player_score += self.state_scanner(" ", " ", disc, " ")
        player_score += self.state_scanner(" ", " ", " ", disc)
        player_score += two_score * self.state_scanner(disc, disc, " ", " ")
        player_score += two_score * self.state_scanner(disc, " ", disc, " ")
        player_score += two_score * self.state_scanner(disc, " ", " ", disc)
        player_score += two_score * self.state_scanner(" ", disc, " ", disc)
        player_score += two_score * self.state_scanner(" ", " ", disc, disc)
        player_score += two_score * self.state_scanner(" ", disc, disc, " ")
        player_score += three_score * self.state_scanner(disc, disc, disc, " ")
        player_score += three_score * self.state_scanner(disc, disc, " ", disc)
        player_score += three_score * self.state_scanner(disc, " ", disc, disc)
        player_score += three_score * self.state_scanner(" ", disc, disc, disc)
        player_score += four_score * self.state_scanner(disc, disc, disc, disc)
        return player_score

    def check_for_win(self, player_disc):
        if self.state_scanner(player_disc, player_disc, player_disc, player_disc) > 0:
            return True
        else:
            return False
