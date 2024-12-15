import tkinter as tk
from tkinter import messagebox
import winsound  # For sound effects
from game_logic import TicTacToeLogic


class TicTacToeGUI:
    def __init__(self):
        self.logic = TicTacToeLogic()
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x600")
        self.buttons = []
        self.single_player = None  # Game mode (None initially)
        self.themes = {
            "Classic": {"bg": "#f5f5f5", "btn_bg": "#ddf", "btn_active": "#add8e6", "score_bg": "#ffffff"},
            "Blue Ocean": {"bg": "#e1f5fe", "btn_bg": "#81d4fa", "btn_active": "#0288d1", "score_bg": "#80deea"},
            "Nature": {"bg": "#e3f2fd", "btn_bg": "#a5d6a7", "btn_active": "#66bb6a", "score_bg": "#c8e6c9"},
            "Retro": {"bg": "#f9e5b8", "btn_bg": "#f4b400", "btn_active": "#d68b00", "score_bg": "#ffcc00"},
        }
        self.current_theme = "Classic"
        self.create_widgets()

    def create_widgets(self):
        # Scoreboard
        self.score_label = tk.Label(
            self.root, text="Player X: 0 | Player O: 0", font=("Arial", 14), bg="#f5f5f5"
        )
        self.score_label.pack(pady=10)

        # Create a 3x3 grid of buttons
        self.board_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.board_frame.pack(pady=10)
        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 18),
                width=5,
                height=2,
                bg="#ddf",
                activebackground="#add8e6",
                relief="raised",
                state="disabled",  # Disabled until a mode is selected
                command=lambda i=i: self.on_button_click(i),
            )
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        # Game mode selection
        self.mode_label = tk.Label(
            self.root, text="Select Mode:", font=("Arial", 12), bg="#f5f5f5"
        )
        self.mode_label.pack(pady=5)
        mode_frame = tk.Frame(self.root, bg="#f5f5f5")
        mode_frame.pack(pady=5)
        tk.Button(
            mode_frame, text="Single Player", font=("Arial", 12), bg="#90ee90", command=self.set_single_player
        ).pack(side="left", padx=5)
        tk.Button(
            mode_frame, text="Two Players", font=("Arial", 12), bg="#ffa07a", command=self.set_two_player
        ).pack(side="left", padx=5)

        # Theme selector
        self.theme_label = tk.Label(self.root, text="Select Theme:", font=("Arial", 12), bg="#f5f5f5")
        self.theme_label.pack(pady=5)
        theme_frame = tk.Frame(self.root, bg="#f5f5f5")
        theme_frame.pack(pady=5)
        for theme in self.themes.keys():
            tk.Button(
                theme_frame, text=theme, font=("Arial", 12), bg="#b0bec5", command=lambda t=theme: self.set_theme(t)
            ).pack(side="left", padx=5)

        # Reset button
        reset_button = tk.Button(
            self.root, text="Reset Game", font=("Arial", 14), bg="#ffc107", command=self.reset_game
        )
        reset_button.pack(pady=10)

    def play_sound(self, sound_file):
        """Plays a sound effect."""
        try:
            winsound.PlaySound(f"assets/{sound_file}", winsound.SND_ASYNC)
        except Exception as e:
            print(f"Sound error: {e}")

    def update_scoreboard(self):
        self.score_label.config(
            text=f"Player X: {self.logic.scores['X']} | Player O: {self.logic.scores['O']}"
        )

    def on_button_click(self, index):
        if self.buttons[index]["text"] == "":
            self.play_sound("move.wav")
            move_result = self.logic.make_move(index)
            self.buttons[index]["text"] = self.logic.board[index]
            self.buttons[index].config(bg="#aad", disabledforeground="black")
            if move_result:
                self.play_sound("win.wav")  # Different sound when a player wins
                messagebox.showinfo("Game Over", move_result)
                self.update_scoreboard()
                self.reset_game()
                return
            if self.single_player and self.logic.current_player == "O":
                self.root.after(500, self.ai_move)

    def ai_move(self):
        ai_index = self.logic.ai_move()
        if ai_index is not None:
            self.on_button_click(ai_index)

    def reset_game(self):
        self.logic.reset_board()
        for button in self.buttons:
            button["text"] = ""
            button.config(bg="#ddf")
        self.play_sound("reset.wav")

    def set_single_player(self):
        self.single_player = True
        self.enable_buttons()
        messagebox.showinfo("Game Mode", "Single Player game started!")

    def set_two_player(self):
        self.single_player = False
        self.enable_buttons()
        messagebox.showinfo("Game Mode", "Two Players game started!")

    def enable_buttons(self):
        """Enables the buttons on the board."""
        for button in self.buttons:
            button.config(state="normal")

    def set_theme(self, theme):
        """Applies the selected theme."""
        self.current_theme = theme
        theme_colors = self.themes[theme]
        self.root.configure(bg=theme_colors["bg"])
        self.score_label.config(bg=theme_colors["score_bg"])
        self.board_frame.config(bg=theme_colors["bg"])
        for button in self.buttons:
            button.config(bg=theme_colors["btn_bg"], activebackground=theme_colors["btn_active"])

    def run(self):
        self.root.configure(bg="#f5f5f5")
        self.root.mainloop()
