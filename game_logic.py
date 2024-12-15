import random

class TicTacToeLogic:
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.scores = {"X": 0, "O": 0}  # Scoreboard

    def make_move(self, index):
        if self.board[index] == "":
            self.board[index] = self.current_player
            if self.check_winner():
                self.scores[self.current_player] += 1
                return f"Player {self.current_player} wins!"
            elif "" not in self.board:
                return "It's a draw!"
            self.current_player = "O" if self.current_player == "X" else "X"
        return None

    def check_winner(self):
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]             # Diagonals
        ]
        for combo in win_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "":
                return True
        return False

    def reset_board(self):
        self.board = [""] * 9
        self.current_player = "X"

    def get_empty_spots(self):
        return [i for i, spot in enumerate(self.board) if spot == ""]

    def ai_move(self):
        empty_spots = self.get_empty_spots()
        if empty_spots:
            return random.choice(empty_spots)
        return None