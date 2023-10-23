from timeit import default_timer as timer
from . import boards, players


messages = {"invalid": "Not a valid choice.", "quit": "Exiting the program."}


def choose_replay(player_X, player_O, board, display_options=True):
    if display_options:
        print("Please choose one of the following options listed below.")
        print(
            "  1: Play again\n  2: Change who plays the game\n  3: Choose a different game\n  4: Exit"
        )
    choice = input("Enter your choice here: ").strip()
    # Replay game
    if choice == "1":
        play_game(player_X, player_O, board)
    # Change who plays the game
    elif choice == "2":
        choose_player_mode(board)
    # Choose a different game
    elif choice == "3":
        choose_game()
    # Quit program
    elif choice == "4":
        print(messages["quit"])
        quit()
    # Invalid choice
    else:
        print(messages["invalid"])
        choose_replay(player_X, player_O, board, display_options=False)


def play_game(player_X, player_O, board):
    board.reset_board()
    winner = ""
    print("A new game has been started.")
    board.print_board()
    current_player = player_X
    while winner == "":
        start = timer()
        current_player_move = current_player.move(board)
        end = timer()
        board.place_disc(current_player.disc, current_player_move, "game")
        board.print_board()
        print(f"Player {current_player.disc} chose move {current_player_move}.")
        print(f"Decision time: {round(end - start, 3)} seconds")
        if board.check_for_win(current_player.disc):
            winner = current_player.disc
        elif board.board_full():
            winner = "draw"
        else:
            if current_player == player_X:
                current_player = player_O
            else:
                current_player = player_X
    if winner == "draw":
        print("Game ended in a draw.")
    else:
        print(f"Player {winner} wins! Game Over.")
    choose_replay(player_X, player_O, board)


def choose_piece(board, display_options=True):
    if display_options:
        print(
            f"Do you want to play as {board.disc_1} or {board.disc_2} against the computer? {board.disc_1} has the first move."
        )

    choice = None
    while choice is None:
        choice = input("Enter your choice here: ").strip().upper()

        if choice not in [board.disc_1, board.disc_2]:
            choice = None
            print(messages["invalid"])

    return choice


def choose_player_mode(board, display_options=True):
    if display_options:
        print("Please choose one of the following options listed below.")
        print(
            "  1: Player vs Player\n  2: Player vs Computer\n  3: Computer vs Computer\n  4: Choose a different game\n  5: Exit"
        )
    choice = input("Enter your choice here: ").strip()
    # Human vs Human
    if choice == "1":
        play_game(
            players.Human(board.disc_1, board.disc_2),
            players.Human(board.disc_2, board.disc_1),
            board,
        )
    # Human vs Computer
    elif choice == "2":
        chosen_piece = choose_piece(board)
        if chosen_piece.upper() == board.disc_1:
            play_game(
                players.Human(board.disc_1, board.disc_2),
                players.Computer(board.disc_2, board.disc_1),
                board,
            )
        elif chosen_piece.upper() == board.disc_2:
            play_game(
                players.Computer(board.disc_1, board.disc_2),
                players.Human(board.disc_2, board.disc_1),
                board,
            )
    # Robot wars
    elif choice == "3":
        play_game(
            players.Computer(board.disc_1, board.disc_2),
            players.Computer(board.disc_2, board.disc_1),
            board,
        )
    # Different game
    elif choice == "4":
        choose_game()
    # Quit program
    elif choice == "5":
        print(messages["quit"])
        quit()
    # Invalid choice
    else:
        print(messages["invalid"])
        choose_player_mode(board, display_options=False)


def choose_game(display_options=True):
    if display_options:
        print("Please choose one of the following options listed below.")
        print("  1: Connect4\n  2: Tic-tac-toe\n  3: Exit")
    choice = input("Enter your choice here: ").strip()
    # Connect4
    if choice == "1":
        print("LETS PLAY CONNECT4.")
        board = boards.Connect4()
        choose_player_mode(board)
    # Tic-tac-toe
    elif choice == "2":
        print("LETS PLAY TIC-TAC-TOE.")
        board = boards.Tictactoe()
        choose_player_mode(board)
    # Quit program
    elif choice == "3":
        print(messages["quit"])
        quit()
    # Invalid choice
    else:
        print(messages["invalid"])
        choose_game(display_options=False)


def run():
    print("Welcome to Command Line Board Games.")
    choose_game()
