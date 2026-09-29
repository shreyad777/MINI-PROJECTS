import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

# ============================================================
# NUMBER GUESSING GAME V30
# COMPETITIVE MODE EDITION
# ============================================================

SAVE_FILE = "leaderboard_v30.json"
PROFILE_FILE = "player_profile_v30.json"
ACHIEVEMENT_FILE = "achievements_v30.json"
STATS_FILE = "game_statistics_v30.json"

# ============================================================
# COLORS
# ============================================================

BG = "#0B1020"
PANEL = "#151C35"
PANEL2 = "#1D2747"

PURPLE = "#9B59FF"
BLUE = "#4D9EFF"
CYAN = "#35D9FF"
GREEN = "#32E875"
YELLOW = "#FFD43B"
ORANGE = "#FF9F43"
RED = "#FF5C5C"
PINK = "#FF5DA2"

WHITE = "#FFFFFF"
GRAY = "#AAB4D0"

# ============================================================
# DIFFICULTY
# ============================================================

DIFFICULTIES = {
    "Easy": {
        "max": 50,
        "attempts": 15,
        "time": 90,
        "score": 100
    },
    "Medium": {
        "max": 100,
        "attempts": 10,
        "time": 60,
        "score": 200
    },
    "Hard": {
        "max": 500,
        "attempts": 7,
        "time": 45,
        "score": 300
    }
}

# ============================================================
# ACHIEVEMENTS
# ============================================================

ACHIEVEMENTS = {
    "first_win": {
        "name": "First Blood",
        "description": "Win your first game",
        "icon": "🥉",
        "xp": 100
    },
    "sharp_shooter": {
        "name": "Sharp Shooter",
        "description": "Win within 3 guesses",
        "icon": "🎯",
        "xp": 125
    },
    "on_fire": {
        "name": "On Fire",
        "description": "Reach a 3-win streak",
        "icon": "🔥",
        "xp": 150
    },
    "power_player": {
        "name": "Power Player",
        "description": "Use a power-up and win",
        "icon": "⚡",
        "xp": 125
    },
    "high_roller": {
        "name": "High Roller",
        "description": "Score 300+",
        "icon": "💯",
        "xp": 150
    },
    "no_help": {
        "name": "No Help Needed",
        "description": "Win without power-ups",
        "icon": "🧠",
        "xp": 150
    },
    "speed_demon": {
        "name": "Speed Demon",
        "description": "Win with 10+ seconds remaining",
        "icon": "⚡",
        "xp": 150
    },
    "hard_mode": {
        "name": "Hard Mode Hero",
        "description": "Win on Hard",
        "icon": "💀",
        "xp": 200
    },
    "five_streak": {
        "name": "Unstoppable",
        "description": "Reach a 5-win streak",
        "icon": "👑",
        "xp": 250
    },
    "level_five": {
        "name": "Rising Star",
        "description": "Reach Level 5",
        "icon": "⭐",
        "xp": 300
    }
}


# ============================================================
# FILE FUNCTIONS
# ============================================================

def load_json(filename, default):

    try:
        if os.path.exists(filename):

            with open(
                filename,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

    except Exception:
        pass

    return default


def save_json(filename, data):

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except Exception:
        pass


# ============================================================
# MAIN CLASS
# ============================================================

class NumberGuessingGame:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Number Guessing Game V30"
        )

        self.root.geometry(
            "1250x760"
        )

        self.root.configure(
            bg=BG
        )

        self.root.resizable(
            False,
            False
        )

        # ----------------------------------------------------
        # PROFILE
        # ----------------------------------------------------

        self.player_name = "Player"

        self.profile = load_json(
            PROFILE_FILE,
            {
                "xp": 0,
                "level": 1,
                "total_wins": 0,
                "total_games": 0,
                "best_streak": 0
            }
        )

        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        self.statistics = load_json(
            STATS_FILE,
            {
                "highest_score": 0,
                "highest_level": 1,
                "total_xp_earned": 0,
                "total_guesses": 0,
                "completed_quests": 0,
                "difficulty": {
                    "Easy": {
                        "games": 0,
                        "wins": 0,
                        "score": 0
                    },
                    "Medium": {
                        "games": 0,
                        "wins": 0,
                        "score": 0
                    },
                    "Hard": {
                        "games": 0,
                        "wins": 0,
                        "score": 0
                    }
                }
            }
        )

        # ----------------------------------------------------
        # ACHIEVEMENTS
        # ----------------------------------------------------

        self.achievements = load_json(
            ACHIEVEMENT_FILE,
            {}
        )

        # ----------------------------------------------------
        # LEADERBOARD
        # ----------------------------------------------------

        self.leaderboard = load_json(
            SAVE_FILE,
            []
        )

        # ----------------------------------------------------
        # GAME STATE
        # ----------------------------------------------------

        self.secret_number = 0

        self.attempts_left = 0

        self.current_score = 0

        self.start_time = 0

        self.time_left = 0

        self.timer_running = False

        self.streak = 0

        self.combo = 1

        self.current_difficulty = "Easy"

        # ----------------------------------------------------
        # POWER UPS
        # ----------------------------------------------------

        self.extra_life = True
        self.time_freeze = True
        self.double_score = True
        self.reveal_range = True

        self.power_used = False

        # ----------------------------------------------------
        # MODE
        # ----------------------------------------------------

        self.mode = "Single Player"

        # ----------------------------------------------------
        # COMPETITIVE STATE
        # ----------------------------------------------------

        self.player1_name = "Player 1"
        self.player2_name = "Player 2"

        self.player1_score = 0
        self.player2_score = 0

        self.current_turn = 1

        self.round_number = 1
        self.total_rounds = 3

        self.tournament_active = False

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.build_ui()

        self.new_game()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        tk.Label(
            self.root,
            text="🎯 NUMBER GUESSING ARCADE",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(
            pady=(15, 2)
        )

        tk.Label(
            self.root,
            text="V30 • COMPETITIVE MODE EDITION",
            font=("Segoe UI", 10, "bold"),
            bg=BG,
            fg=PURPLE
        ).pack()

        # ----------------------------------------------------
        # MAIN
        # ----------------------------------------------------

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True,
            padx=18,
            pady=15
        )

        # ====================================================
        # LEFT PANEL
        # ====================================================

        left = tk.Frame(
            main,
            bg=PANEL,
            width=250,
            height=620
        )

        left.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="⚙ GAME SETTINGS",
            font=("Segoe UI", 14, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(
            pady=18
        )

        tk.Label(
            left,
            text="Player Name",
            bg=PANEL,
            fg=GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack()

        self.name_entry = tk.Entry(
            left,
            font=("Segoe UI", 11),
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            justify="center"
        )

        self.name_entry.insert(
            0,
            self.player_name
        )

        self.name_entry.pack(
            pady=7,
            padx=25,
            fill="x"
        )

        tk.Label(
            left,
            text="Difficulty",
            bg=PANEL,
            fg=GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=(15, 3)
        )

        self.difficulty_var = tk.StringVar(
            value="Easy"
        )

        for difficulty in DIFFICULTIES:

            tk.Radiobutton(
                left,
                text=difficulty,
                variable=self.difficulty_var,
                value=difficulty,
                command=self.new_game,
                bg=PANEL,
                fg=WHITE,
                selectcolor=PANEL2,
                activebackground=PANEL,
                activeforeground=CYAN,
                font=("Segoe UI", 10)
            ).pack(
                anchor="w",
                padx=35
            )

        # ----------------------------------------------------
        # GAME MODE
        # ----------------------------------------------------

        tk.Label(
            left,
            text="Game Mode",
            bg=PANEL,
            fg=GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=(18, 3)
        )

        self.mode_var = tk.StringVar(
            value="Single Player"
        )

        for mode in [
            "Single Player",
            "Two Player",
            "Tournament"
        ]:

            tk.Radiobutton(
                left,
                text=mode,
                variable=self.mode_var,
                value=mode,
                command=self.change_mode,
                bg=PANEL,
                fg=WHITE,
                selectcolor=PANEL2,
                activebackground=PANEL,
                activeforeground=CYAN,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                padx=35
            )

        # ----------------------------------------------------
        # BUTTONS
        # ----------------------------------------------------

        tk.Button(
            left,
            text="👤 PLAYER PROFILE",
            command=self.show_profile,
            bg=PURPLE,
            fg=WHITE,
            activebackground=BLUE,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=(20, 7),
            padx=25,
            fill="x"
        )

        tk.Button(
            left,
            text="🏆 LEADERBOARD",
            command=self.show_leaderboard,
            bg=BLUE,
            fg=WHITE,
            activebackground=CYAN,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=5,
            padx=25,
            fill="x"
        )

        tk.Button(
            left,
            text="🎖 ACHIEVEMENTS",
            command=self.show_achievements,
            bg=ORANGE,
            fg=WHITE,
            activebackground=YELLOW,
            relief="flat",
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=5,
            padx=25,
            fill="x"
        )

        # ====================================================
        # CENTER
        # ====================================================

        center = tk.Frame(
            main,
            bg=PANEL,
            width=600,
            height=620
        )

        center.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        center.pack_propagate(False)

        self.status_label = tk.Label(
            center,
            text="Guess the secret number!",
            font=("Segoe UI", 15, "bold"),
            bg=PANEL,
            fg=WHITE
        )

        self.status_label.pack(
            pady=(20, 10)
        )

        # ----------------------------------------------------
        # COMPETITIVE SCOREBOARD
        # ----------------------------------------------------

        self.competitive_label = tk.Label(
            center,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=PINK
        )

        self.competitive_label.pack(
            pady=3
        )

        self.turn_label = tk.Label(
            center,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=YELLOW
        )

        self.turn_label.pack(
            pady=3
        )

        # ----------------------------------------------------
        # ROUND
        # ----------------------------------------------------

        self.round_label = tk.Label(
            center,
            text="",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=PURPLE
        )

        self.round_label.pack(
            pady=3
        )

        # ----------------------------------------------------
        # TIMER
        # ----------------------------------------------------

        self.timer_label = tk.Label(
            center,
            text="⏱ 00s",
            font=("Segoe UI", 18, "bold"),
            bg=PANEL,
            fg=YELLOW
        )

        self.timer_label.pack(
            pady=5
        )

        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        self.score_label = tk.Label(
            center,
            text="⭐ Score: 0",
            font=("Segoe UI", 13, "bold"),
            bg=PANEL,
            fg=GREEN
        )

        self.score_label.pack()

        # ----------------------------------------------------
        # STREAK
        # ----------------------------------------------------

        self.streak_label = tk.Label(
            center,
            text="🔥 Streak: 0   Combo: x1",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL,
            fg=ORANGE
        )

        self.streak_label.pack(
            pady=5
        )

        # ----------------------------------------------------
        # RANGE
        # ----------------------------------------------------

        self.range_label = tk.Label(
            center,
            text="",
            font=("Segoe UI", 12),
            bg=PANEL,
            fg=CYAN
        )

        self.range_label.pack(
            pady=15
        )

        # ----------------------------------------------------
        # GUESS
        # ----------------------------------------------------

        self.guess_entry = tk.Entry(
            center,
            font=("Segoe UI", 22, "bold"),
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            justify="center"
        )

        self.guess_entry.pack(
            padx=100,
            fill="x",
            ipady=8
        )

        self.guess_entry.bind(
            "<Return>",
            lambda event: self.check_guess()
        )

        tk.Button(
            center,
            text="🎯 MAKE GUESS",
            command=self.check_guess,
            bg=GREEN,
            fg=BG,
            activebackground=CYAN,
            relief="flat",
            font=("Segoe UI", 13, "bold")
        ).pack(
            pady=12,
            ipadx=20,
            ipady=6
        )

        self.attempts_label = tk.Label(
            center,
            text="Attempts: 0",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=WHITE
        )

        self.attempts_label.pack()

        # ----------------------------------------------------
        # POWER UPS
        # ----------------------------------------------------

        power_frame = tk.Frame(
            center,
            bg=PANEL
        )

        power_frame.pack(
            pady=10
        )

        tk.Label(
            power_frame,
            text="⚡ POWER-UPS",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack()

        power_buttons = tk.Frame(
            power_frame,
            bg=PANEL
        )

        power_buttons.pack(
            pady=6
        )

        self.life_button = tk.Button(
            power_buttons,
            text="❤️ +2",
            command=self.use_extra_life,
            bg=RED,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        self.life_button.pack(
            side="left",
            padx=3
        )

        self.freeze_button = tk.Button(
            power_buttons,
            text="❄️ FREEZE",
            command=self.use_time_freeze,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        self.freeze_button.pack(
            side="left",
            padx=3
        )

        self.double_button = tk.Button(
            power_buttons,
            text="⭐ 2X",
            command=self.use_double_score,
            bg=YELLOW,
            fg=BG,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        self.double_button.pack(
            side="left",
            padx=3
        )

        self.range_button = tk.Button(
            power_buttons,
            text="🔍 RANGE",
            command=self.use_reveal_range,
            bg=PURPLE,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        self.range_button.pack(
            side="left",
            padx=3
        )

        tk.Button(
            center,
            text="🔄 NEW GAME",
            command=self.new_game,
            bg=PANEL2,
            fg=WHITE,
            activebackground=PURPLE,
            relief="flat",
            font=("Segoe UI", 11, "bold")
        ).pack(
            pady=5
        )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right = tk.Frame(
            main,
            bg=PANEL,
            width=260,
            height=620
        )

        right.pack(
            side="right",
            fill="y",
            padx=(10, 0)
        )

        right.pack_propagate(False)

        tk.Label(
            right,
            text="👤 PLAYER",
            font=("Segoe UI", 14, "bold"),
            bg=PANEL,
            fg=CYAN
        ).pack(
            pady=(18, 5)
        )

        self.player_display = tk.Label(
            right,
            text="Player",
            font=("Segoe UI", 13, "bold"),
            bg=PANEL,
            fg=WHITE
        )

        self.player_display.pack()

        self.level_display = tk.Label(
            right,
            text="⭐ Level 1",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=YELLOW
        )

        self.level_display.pack(
            pady=5
        )

        self.xp_label = tk.Label(
            right,
            text="XP: 0",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=GREEN
        )

        self.xp_label.pack(
            pady=(10, 2)
        )

        self.xp_bar = tk.Canvas(
            right,
            width=210,
            height=16,
            bg=PANEL2,
            highlightthickness=0
        )

        self.xp_bar.pack(
            pady=3
        )

        tk.Label(
            right,
            text="📊 QUICK STATS",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack(
            pady=(20, 10)
        )

        self.quick_stats = tk.Label(
            right,
            text="",
            justify="left",
            anchor="w",
            font=("Segoe UI", 10),
            bg=PANEL,
            fg=WHITE
        )

        self.quick_stats.pack(
            padx=20,
            fill="x"
        )

        tk.Label(
            right,
            text="🏆 COMPETITIVE SCORE",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=ORANGE
        ).pack(
            pady=(25, 8)
        )

        self.competitive_side = tk.Label(
            right,
            text="",
            justify="left",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=WHITE
        )

        self.competitive_side.pack()

        self.update_profile_display()

    # ========================================================
    # MODE CHANGE
    # ========================================================

    def change_mode(self):

        self.mode = self.mode_var.get()

        self.timer_running = False

        if self.mode == "Single Player":

            self.new_game()

        elif self.mode == "Two Player":

            self.start_two_player()

        elif self.mode == "Tournament":

            self.start_tournament()

    # ========================================================
    # NEW GAME
    # ========================================================

    def new_game(self):

        self.player_name = (
            self.name_entry.get().strip()
            or "Player"
        )

        self.player_display.config(
            text=self.player_name
        )

        self.current_difficulty = (
            self.difficulty_var.get()
        )

        self.mode = self.mode_var.get()

        # ----------------------------------------------------
        # COMPETITIVE MODES
        # ----------------------------------------------------

        if self.mode == "Two Player":

            self.start_two_player()

            return

        if self.mode == "Tournament":

            self.start_tournament()

            return

        # ----------------------------------------------------
        # SINGLE PLAYER
        # ----------------------------------------------------

        difficulty = DIFFICULTIES[
            self.current_difficulty
        ]

        self.secret_number = random.randint(
            1,
            difficulty["max"]
        )

        self.attempts_left = difficulty[
            "attempts"
        ]

        self.current_score = difficulty[
            "score"
        ]

        self.time_left = difficulty[
            "time"
        ]

        self.timer_running = True

        self.start_time = time.time()

        self.extra_life = True
        self.time_freeze = True
        self.double_score = True
        self.reveal_range = True

        self.power_used = False

        self.life_button.config(
            state="normal"
        )

        self.freeze_button.config(
            state="normal"
        )

        self.double_button.config(
            state="normal"
        )

        self.range_button.config(
            state="normal"
        )

        self.guess_entry.config(
            state="normal"
        )

        self.guess_entry.delete(
            0,
            tk.END
        )

        self.status_label.config(
            text="🎯 Guess the secret number!"
        )

        self.competitive_label.config(
            text=""
        )

        self.turn_label.config(
            text=""
        )

        self.round_label.config(
            text=""
        )

        self.range_label.config(
            text=(
                f"Number is between "
                f"1 and {difficulty['max']}"
            )
        )

        self.update_game_display()

        self.timer_tick()

    # ========================================================
    # TWO PLAYER
    # ========================================================

    def start_two_player(self):

        self.timer_running = False

        self.player1_name = (
            self.name_entry.get().strip()
            or "Player 1"
        )

        self.player2_name = "Player 2"

        self.player1_score = 0
        self.player2_score = 0

        self.current_turn = 1

        self.tournament_active = False

        self.start_competitive_round()

    # ========================================================
    # TOURNAMENT
    # ========================================================

    def start_tournament(self):

        self.timer_running = False

        self.player1_name = (
            self.name_entry.get().strip()
            or "Player 1"
        )

        self.player2_name = "Player 2"

        self.player1_score = 0
        self.player2_score = 0

        self.current_turn = 1

        self.round_number = 1

        self.total_rounds = 3

        self.tournament_active = True

        self.start_competitive_round()

    # ========================================================
    # COMPETITIVE ROUND
    # ========================================================

    def start_competitive_round(self):

        difficulty = DIFFICULTIES[
            self.difficulty_var.get()
        ]

        self.current_difficulty = (
            self.difficulty_var.get()
        )

        self.secret_number = random.randint(
            1,
            difficulty["max"]
        )

        self.attempts_left = difficulty[
            "attempts"
        ]

        self.time_left = difficulty[
            "time"
        ]

        self.current_score = difficulty[
            "score"
        ]

        self.current_turn = 1

        self.timer_running = True

        self.guess_entry.config(
            state="normal"
        )

        self.guess_entry.delete(
            0,
            tk.END
        )

        self.status_label.config(
            text="🎯 Find the secret number!"
        )

        if self.tournament_active:

            self.round_label.config(
                text=(
                    f"🏆 ROUND "
                    f"{self.round_number}/"
                    f"{self.total_rounds}"
                )
            )

        else:

            self.round_label.config(
                text="👥 TWO PLAYER ROUND"
            )

        self.update_competitive_display()

        self.timer_tick()

    # ========================================================
    # TIMER
    # ========================================================

    def timer_tick(self):

        if not self.timer_running:
            return

        if self.time_left <= 0:

            self.timer_running = False

            if self.mode in [
                "Two Player",
                "Tournament"
            ]:

                self.competitive_loss(
                    "⏰ Time's up!"
                )

            else:

                self.end_single_loss(
                    "⏰ Time's up!"
                )

            return

        self.timer_label.config(
            text=f"⏱ {self.time_left:02d}s"
        )

        self.time_left -= 1

        self.root.after(
            1000,
            self.timer_tick
        )

    # ========================================================
    # CHECK GUESS
    # ========================================================

    def check_guess(self):

        if not self.timer_running:
            return

        value = self.guess_entry.get().strip()

        if not value.isdigit():

            messagebox.showwarning(
                "Invalid Input",
                "Please enter a valid number."
            )

            return

        guess = int(value)

        maximum = DIFFICULTIES[
            self.current_difficulty
        ]["max"]

        if guess < 1 or guess > maximum:

            messagebox.showwarning(
                "Out of Range",
                f"Enter a number between 1 and {maximum}."
            )

            return

        self.attempts_left -= 1

        self.statistics[
            "total_guesses"
        ] += 1

        # ----------------------------------------------------
        # CORRECT
        # ----------------------------------------------------

        if guess == self.secret_number:

            self.timer_running = False

            if self.mode in [
                "Two Player",
                "Tournament"
            ]:

                self.competitive_win()

            else:

                guesses_used = (
                    DIFFICULTIES[
                        self.current_difficulty
                    ]["attempts"]
                    - self.attempts_left
                )

                self.single_player_win(
                    guesses_used
                )

            return

        # ----------------------------------------------------
        # WRONG
        # ----------------------------------------------------

        if guess < self.secret_number:

            self.status_label.config(
                text="📈 Too Low!"
            )

        else:

            self.status_label.config(
                text="📉 Too High!"
            )

        if self.attempts_left <= 0:

            self.timer_running = False

            if self.mode in [
                "Two Player",
                "Tournament"
            ]:

                self.competitive_loss(
                    f"💥 Out of attempts!\n"
                    f"The number was "
                    f"{self.secret_number}."
                )

            else:

                self.end_single_loss(
                    f"💥 Out of attempts!\n"
                    f"The number was "
                    f"{self.secret_number}."
                )

            return

        self.update_game_display()

    # ========================================================
    # SINGLE PLAYER WIN
    # ========================================================

    def single_player_win(
        self,
        guesses_used
    ):

        self.profile[
            "total_games"
        ] += 1

        self.profile[
            "total_wins"
        ] += 1

        self.streak += 1

        if self.streak > self.profile[
            "best_streak"
        ]:

            self.profile[
                "best_streak"
            ] = self.streak

        if self.streak >= 5:

            self.combo = 3

        elif self.streak >= 3:

            self.combo = 2

        else:

            self.combo = 1

        score = self.current_score

        score += self.attempts_left * 10

        score += self.time_left * 2

        score *= self.combo

        if self.double_score:

            score *= 2

        self.current_score = score

        self.statistics[
            "highest_score"
        ] = max(
            self.statistics[
                "highest_score"
            ],
            score
        )

        difficulty_stats = (
            self.statistics[
                "difficulty"
            ][self.current_difficulty]
        )

        difficulty_stats[
            "games"
        ] += 1

        difficulty_stats[
            "wins"
        ] += 1

        difficulty_stats[
            "score"
        ] += score

        self.add_xp(100)

        self.check_achievements(
            guesses_used
        )

        self.save_all()

        self.update_profile_display()

        self.record_leaderboard()

        messagebox.showinfo(
            "🎉 YOU WIN!",
            f"Congratulations "
            f"{self.player_name}!\n\n"
            f"Secret Number: "
            f"{self.secret_number}\n"
            f"Guesses Used: "
            f"{guesses_used}\n"
            f"Score: {score}\n"
            f"Streak: {self.streak}\n"
            f"Combo: x{self.combo}"
        )

    # ========================================================
    # SINGLE PLAYER LOSS
    # ========================================================

    def end_single_loss(
        self,
        message
    ):

        self.profile[
            "total_games"
        ] += 1

        self.streak = 0
        self.combo = 1

        self.statistics[
            "difficulty"
        ][self.current_difficulty][
            "games"
        ] += 1

        self.save_all()

        self.update_profile_display()

        messagebox.showinfo(
            "Game Over",
            message
        )

    # ========================================================
    # COMPETITIVE WIN
    # ========================================================

    def competitive_win(self):

        winner = (
            self.player1_name
            if self.current_turn == 1
            else self.player2_name
        )

        points = max(
            50,
            self.current_score
            + self.attempts_left * 10
            + self.time_left
        )

        if self.current_turn == 1:

            self.player1_score += points

        else:

            self.player2_score += points

        self.timer_running = False

        self.update_competitive_display()

        messagebox.showinfo(
            "🏆 ROUND WINNER!",
            f"🎉 {winner} wins the round!\n\n"
            f"Secret Number: "
            f"{self.secret_number}\n"
            f"Points Earned: {points}\n\n"
            f"{self.player1_name}: "
            f"{self.player1_score}\n"
            f"{self.player2_name}: "
            f"{self.player2_score}"
        )

        if self.mode == "Tournament":

            self.next_tournament_round()

        else:

            self.finish_two_player_round()

    # ========================================================
    # COMPETITIVE LOSS
    # ========================================================

    def competitive_loss(
        self,
        message
    ):

        loser = (
            self.player1_name
            if self.current_turn == 1
            else self.player2_name
        )

        self.timer_running = False

        messagebox.showinfo(
            "Round Over",
            f"{message}\n\n"
            f"{loser} lost the round."
        )

        if self.mode == "Tournament":

            self.next_tournament_round()

        else:

            self.finish_two_player_round()

    # ========================================================
    # TWO PLAYER NEXT TURN
    # ========================================================

    def finish_two_player_round(self):

        if self.current_turn == 1:

            self.current_turn = 2

            self.start_player_turn()

        else:

            self.show_two_player_result()

    # ========================================================
    # PLAYER TURN
    # ========================================================

    def start_player_turn(self):

        difficulty = DIFFICULTIES[
            self.current_difficulty
        ]

        self.secret_number = random.randint(
            1,
            difficulty["max"]
        )

        self.attempts_left = difficulty[
            "attempts"
        ]

        self.time_left = difficulty[
            "time"
        ]

        self.current_score = difficulty[
            "score"
        ]

        self.guess_entry.delete(
            0,
            tk.END
        )

        self.timer_running = True

        current_player = (
            self.player1_name
            if self.current_turn == 1
            else self.player2_name
        )

        self.status_label.config(
            text=(
                f"🎯 {current_player}'s turn"
            )
        )

        self.turn_label.config(
            text=(
                f"🎮 TURN: "
                f"{current_player}"
            )
        )

        self.update_competitive_display()

        self.timer_tick()

    # ========================================================
    # TWO PLAYER RESULT
    # ========================================================

    def show_two_player_result(self):

        self.timer_running = False

        if self.player1_score > self.player2_score:

            winner = self.player1_name

        elif self.player2_score > self.player1_score:

            winner = self.player2_name

        else:

            winner = "DRAW"

        if winner == "DRAW":

            result = (
                "🤝 IT'S A DRAW!\n\n"
                f"{self.player1_name}: "
                f"{self.player1_score}\n"
                f"{self.player2_name}: "
                f"{self.player2_score}"
            )

        else:

            result = (
                f"🏆 {winner} WINS!\n\n"
                f"{self.player1_name}: "
                f"{self.player1_score}\n"
                f"{self.player2_name}: "
                f"{self.player2_score}"
            )

        messagebox.showinfo(
            "🏆 MATCH RESULT",
            result
        )

        self.save_all()

        self.new_game()

    # ========================================================
    # TOURNAMENT NEXT ROUND
    # ========================================================

    def next_tournament_round(self):

        if self.round_number >= self.total_rounds:

            self.finish_tournament()

            return

        self.round_number += 1

        self.current_turn = 1

        messagebox.showinfo(
            "🏆 Next Round",
            f"Round {self.round_number} begins!"
        )

        self.start_competitive_round()

    # ========================================================
    # TOURNAMENT RESULT
    # ========================================================

    def finish_tournament(self):

        self.timer_running = False

        if self.player1_score > self.player2_score:

            winner = self.player1_name

        elif self.player2_score > self.player1_score:

            winner = self.player2_name

        else:

            winner = "DRAW"

        if winner == "DRAW":

            result = (
                "🤝 TOURNAMENT DRAW!\n\n"
                f"{self.player1_name}: "
                f"{self.player1_score}\n"
                f"{self.player2_name}: "
                f"{self.player2_score}"
            )

        else:

            result = (
                f"👑 TOURNAMENT CHAMPION\n\n"
                f"🏆 {winner}\n\n"
                f"{self.player1_name}: "
                f"{self.player1_score}\n"
                f"{self.player2_name}: "
                f"{self.player2_score}"
            )

        messagebox.showinfo(
            "🏆 TOURNAMENT COMPLETE!",
            result
        )

        self.tournament_active = False

        self.save_all()

        self.mode_var.set(
            "Single Player"
        )

        self.mode = "Single Player"

        self.new_game()

    # ========================================================
    # COMPETITIVE DISPLAY
    # ========================================================

    def update_competitive_display(self):

        self.competitive_label.config(
            text=(
                f"👤 {self.player1_name}: "
                f"{self.player1_score}"
                f"     VS     "
                f"{self.player2_name}: "
                f"{self.player2_score}"
            )
        )

        if self.mode in [
            "Two Player",
            "Tournament"
        ]:

            current_player = (
                self.player1_name
                if self.current_turn == 1
                else self.player2_name
            )

            self.turn_label.config(
                text=f"🎮 {current_player}'S TURN"
            )

        self.score_label.config(
            text=f"⭐ Score: {self.current_score}"
        )

        self.attempts_label.config(
            text=(
                f"Attempts Remaining: "
                f"{self.attempts_left}"
            )
        )

    # ========================================================
    # POWER UPS
    # ========================================================

    def use_extra_life(self):

        if self.mode != "Single Player":

            return

        if not self.extra_life:

            return

        self.extra_life = False

        self.attempts_left += 2

        self.power_used = True

        self.life_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="❤️ +2 ATTEMPTS!"
        )

        self.update_game_display()

    def use_time_freeze(self):

        if self.mode != "Single Player":

            return

        if not self.time_freeze:

            return

        self.time_freeze = False

        self.power_used = True

        self.freeze_button.config(
            state="disabled"
        )

        self.timer_running = False

        self.status_label.config(
            text="❄️ TIME FROZEN!"
        )

        self.root.after(
            10000,
            self.resume_timer
        )

    def resume_timer(self):

        if not self.timer_running:

            self.timer_running = True

            self.timer_tick()

    def use_double_score(self):

        if self.mode != "Single Player":

            return

        if not self.double_score:

            return

        self.double_score = False

        self.power_used = True

        self.double_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="⭐ 2X SCORE ACTIVATED!"
        )

    def use_reveal_range(self):

        if self.mode != "Single Player":

            return

        if not self.reveal_range:

            return

        self.reveal_range = False

        self.power_used = True

        self.range_button.config(
            state="disabled"
        )

        lower = max(
            1,
            self.secret_number - 10
        )

        upper = min(
            DIFFICULTIES[
                self.current_difficulty
            ]["max"],
            self.secret_number + 10
        )

        self.range_label.config(
            text=(
                f"🔍 Secret is between "
                f"{lower} and {upper}"
            )
        )

    # ========================================================
    # XP
    # ========================================================

    def add_xp(self, amount):

        self.profile["xp"] += amount

        self.statistics[
            "total_xp_earned"
        ] += amount

        while self.profile[
            "xp"
        ] >= self.profile[
            "level"
        ] * 250:

            required = (
                self.profile["level"]
                * 250
            )

            self.profile[
                "xp"
            ] -= required

            self.profile[
                "level"
            ] += 1

            self.statistics[
                "highest_level"
            ] = max(
                self.statistics[
                    "highest_level"
                ],
                self.profile["level"]
            )

            messagebox.showinfo(
                "⭐ LEVEL UP!",
                f"You reached Level "
                f"{self.profile['level']}!"
            )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    def unlock_achievement(
        self,
        key
    ):

        if key in self.achievements:

            return

        achievement = ACHIEVEMENTS[
            key
        ]

        self.achievements[
            key
        ] = True

        self.add_xp(
            achievement["xp"]
        )

        messagebox.showinfo(
            "🏆 Achievement Unlocked!",
            f"{achievement['icon']} "
            f"{achievement['name']}\n\n"
            f"{achievement['description']}\n\n"
            f"+{achievement['xp']} XP"
        )

    def check_achievements(
        self,
        guesses_used
    ):

        if self.profile[
            "total_wins"
        ] == 1:

            self.unlock_achievement(
                "first_win"
            )

        if guesses_used <= 3:

            self.unlock_achievement(
                "sharp_shooter"
            )

        if self.streak >= 3:

            self.unlock_achievement(
                "on_fire"
            )

        if self.power_used:

            self.unlock_achievement(
                "power_player"
            )

        if self.current_score >= 300:

            self.unlock_achievement(
                "high_roller"
            )

        if not self.power_used:

            self.unlock_achievement(
                "no_help"
            )

        if self.time_left >= 10:

            self.unlock_achievement(
                "speed_demon"
            )

        if self.current_difficulty == "Hard":

            self.unlock_achievement(
                "hard_mode"
            )

        if self.streak >= 5:

            self.unlock_achievement(
                "five_streak"
            )

        if self.profile[
            "level"
        ] >= 5:

            self.unlock_achievement(
                "level_five"
            )

    # ========================================================
    # LEADERBOARD
    # ========================================================

    def record_leaderboard(self):

        entry = {
            "name": self.player_name,
            "score": self.current_score,
            "difficulty": self.current_difficulty
        }

        self.leaderboard.append(
            entry
        )

        self.leaderboard.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        self.leaderboard = (
            self.leaderboard[:10]
        )

        save_json(
            SAVE_FILE,
            self.leaderboard
        )

    # ========================================================
    # LEADERBOARD WINDOW
    # ========================================================

    def show_leaderboard(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "🏆 Leaderboard"
        )

        window.geometry(
            "600x500"
        )

        window.configure(
            bg=BG
        )

        tk.Label(
            window,
            text="🏆 TOP PLAYERS",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(
            pady=20
        )

        for index, player in enumerate(
            self.leaderboard,
            start=1
        ):

            text = (
                f"{index}. "
                f"{player['name']}   "
                f"{player['score']} pts   "
                f"({player['difficulty']})"
            )

            tk.Label(
                window,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg=PANEL,
                fg=WHITE,
                anchor="w",
                padx=15
            ).pack(
                fill="x",
                padx=35,
                pady=3
            )

    # ========================================================
    # PROFILE
    # ========================================================

    def show_profile(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "👤 Player Profile"
        )

        window.geometry(
            "720x650"
        )

        window.configure(
            bg=BG
        )

        tk.Label(
            window,
            text="👤 PLAYER PROFILE",
            font=("Segoe UI", 24, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(
            pady=(20, 3)
        )

        tk.Label(
            window,
            text=self.player_name,
            font=("Segoe UI", 16, "bold"),
            bg=BG,
            fg=WHITE
        ).pack()

        tk.Label(
            window,
            text=(
                f"⭐ Level "
                f"{self.profile['level']}"
            ),
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(
            pady=5
        )

        total_games = (
            self.profile["total_games"]
        )

        wins = (
            self.profile["total_wins"]
        )

        losses = max(
            0,
            total_games - wins
        )

        if total_games > 0:

            win_rate = (
                wins / total_games
            ) * 100

        else:

            win_rate = 0

        if total_games > 0:

            average_guesses = (
                self.statistics[
                    "total_guesses"
                ] / total_games
            )

        else:

            average_guesses = 0

        rows = [

            (
                "🎮 Total Games",
                total_games
            ),

            (
                "🏆 Total Wins",
                wins
            ),

            (
                "💥 Total Losses",
                losses
            ),

            (
                "📈 Win Rate",
                f"{win_rate:.1f}%"
            ),

            (
                "💯 Highest Score",
                self.statistics[
                    "highest_score"
                ]
            ),

            (
                "🔥 Best Streak",
                self.profile[
                    "best_streak"
                ]
            ),

            (
                "🎯 Average Guesses",
                f"{average_guesses:.1f}"
            ),

            (
                "⭐ Total XP",
                self.statistics[
                    "total_xp_earned"
                ]
            ),

            (
                "👑 Highest Level",
                self.statistics[
                    "highest_level"
                ]
            ),

            (
                "🎖 Achievements",
                f"{len(self.achievements)}/"
                f"{len(ACHIEVEMENTS)}"
            )
        ]

        frame = tk.Frame(
            window,
            bg=BG
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        for title, value in rows:

            row = tk.Frame(
                frame,
                bg=PANEL
            )

            row.pack(
                fill="x",
                pady=3
            )

            tk.Label(
                row,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg=PANEL,
                fg=WHITE,
                anchor="w"
            ).pack(
                side="left",
                padx=15,
                pady=8
            )

            tk.Label(
                row,
                text=str(value),
                font=("Segoe UI", 10, "bold"),
                bg=PANEL,
                fg=CYAN
            ).pack(
                side="right",
                padx=15
            )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    def show_achievements(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "🎖 Achievement Hall"
        )

        window.geometry(
            "700x620"
        )

        window.configure(
            bg=BG
        )

        tk.Label(
            window,
            text="🎖 ACHIEVEMENT HALL",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=ORANGE
        ).pack(
            pady=15
        )

        tk.Label(
            window,
            text=(
                f"{len(self.achievements)}/"
                f"{len(ACHIEVEMENTS)} Unlocked"
            ),
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(
            pady=(0, 15)
        )

        for key, achievement in (
            ACHIEVEMENTS.items()
        ):

            unlocked = (
                key in self.achievements
            )

            status = (
                "✅ UNLOCKED"
                if unlocked
                else "🔒 LOCKED"
            )

            color = (
                GREEN
                if unlocked
                else GRAY
            )

            row = tk.Frame(
                window,
                bg=PANEL
            )

            row.pack(
                fill="x",
                padx=25,
                pady=4
            )

            tk.Label(
                row,
                text=achievement["icon"],
                font=("Segoe UI Emoji", 18),
                bg=PANEL,
                fg=WHITE
            ).pack(
                side="left",
                padx=10
            )

            tk.Label(
                row,
                text=achievement["name"],
                font=("Segoe UI", 11, "bold"),
                bg=PANEL,
                fg=WHITE
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=status,
                font=("Segoe UI", 9, "bold"),
                bg=PANEL,
                fg=color
            ).pack(
                side="right",
                padx=10
            )

    # ========================================================
    # DISPLAY
    # ========================================================

    def update_game_display(self):

        self.score_label.config(
            text=(
                f"⭐ Score: "
                f"{self.current_score}"
            )
        )

        self.streak_label.config(
            text=(
                f"🔥 Streak: "
                f"{self.streak}"
                f"   Combo: x{self.combo}"
            )
        )

        self.attempts_label.config(
            text=(
                f"Attempts Remaining: "
                f"{self.attempts_left}"
            )
        )

        self.update_profile_display()

    def update_profile_display(self):

        level = self.profile[
            "level"
        ]

        xp = self.profile[
            "xp"
        ]

        self.player_display.config(
            text=self.player_name
        )

        self.level_display.config(
            text=f"⭐ Level {level}"
        )

        required = level * 250

        self.xp_label.config(
            text=f"XP: {xp}/{required}"
        )

        self.xp_bar.delete(
            "all"
        )

        progress = min(
            1,
            xp / required
        )

        self.xp_bar.create_rectangle(
            0,
            0,
            210 * progress,
            16,
            fill=PURPLE,
            outline=""
        )

        total_games = (
            self.profile[
                "total_games"
            ]
        )

        wins = (
            self.profile[
                "total_wins"
            ]
        )

        if total_games:

            win_rate = (
                wins / total_games
            ) * 100

        else:

            win_rate = 0

        self.quick_stats.config(
            text=(
                f"🎮 Games: {total_games}\n"
                f"🏆 Wins: {wins}\n"
                f"📈 Win Rate: "
                f"{win_rate:.1f}%\n"
                f"🔥 Best Streak: "
                f"{self.profile['best_streak']}\n"
                f"💯 High Score: "
                f"{self.statistics['highest_score']}\n"
                f"🎖 Badges: "
                f"{len(self.achievements)}/"
                f"{len(ACHIEVEMENTS)}"
            )
        )

        self.competitive_side.config(
            text=(
                f"{self.player1_name}: "
                f"{self.player1_score}\n\n"
                f"{self.player2_name}: "
                f"{self.player2_score}"
            )
        )

    # ========================================================
    # SAVE EVERYTHING
    # ========================================================

    def save_all(self):

        save_json(
            PROFILE_FILE,
            self.profile
        )

        save_json(
            ACHIEVEMENT_FILE,
            self.achievements
        )

        save_json(
            STATS_FILE,
            self.statistics
        )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = NumberGuessingGame(
        root
    )

    root.mainloop()