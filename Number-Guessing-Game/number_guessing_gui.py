import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time


# ============================================================
# FILES
# ============================================================

LEADERBOARD_FILE = "leaderboard_v30.json"
PROFILE_FILE = "player_profile_v30.json"
ACHIEVEMENTS_FILE = "achievements_v30.json"
STATS_FILE = "game_statistics_v30.json"


# ============================================================
# COLORS
# ============================================================

BG = "#0B1020"
PANEL = "#151C35"
PANEL2 = "#1D2747"

PURPLE = "#A970FF"
BLUE = "#4D8DFF"
CYAN = "#38D9FF"
GREEN = "#4DFF88"
YELLOW = "#FFD84D"
ORANGE = "#FF9D42"
RED = "#FF5C5C"
PINK = "#FF6FD8"

WHITE = "#FFFFFF"
GRAY = "#AAB3CF"


# ============================================================
# GAME
# ============================================================

class NumberGuessingGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game V31")
        self.root.geometry("1100x760")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ---------------- GAME VARIABLES ----------------

        self.player_name = "Player"

        self.mode = "Single Player"
        self.difficulty = "Medium"

        self.number = None
        self.attempts_left = 0
        self.max_attempts = 0
        self.time_limit = 0
        self.time_left = 0

        self.score = 0
        self.total_score = 0
        self.xp = 0
        self.level = 1

        self.streak = 0
        self.combo = 1

        self.game_running = False
        self.timer_id = None

        # V30 competitive variables
        self.player1_score = 0
        self.player2_score = 0

        self.tournament_round = 1
        self.total_rounds = 3
        self.current_turn = 1

        # V31 modes
        self.time_attack_score = 0
        self.time_attack_start = 0

        self.survival_round = 1
        self.survival_lives = 3

        self.endless_round = 1
        self.endless_lives = 3

        self.power_used = False
        self.score_multiplier = 1

        self.extra_life = 0
        self.time_freeze = False

        # ---------------- DIFFICULTY ----------------

        self.difficulties = {
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

        # ---------------- DATA ----------------

        self.profile = self.load_json(
            PROFILE_FILE,
            {
                "name": "Player",
                "xp": 0,
                "level": 1,
                "games": 0,
                "wins": 0,
                "losses": 0,
                "highest_score": 0,
                "best_streak": 0,
                "total_guesses": 0,
                "quests_completed": 0
            }
        )

        self.achievements = self.load_json(
            ACHIEVEMENTS_FILE,
            {}
        )

        self.stats = self.load_json(
            STATS_FILE,
            {
                "Easy": {"games": 0, "wins": 0},
                "Medium": {"games": 0, "wins": 0},
                "Hard": {"games": 0, "wins": 0}
            }
        )

        self.profile_name = self.profile.get("name", "Player")

        self.build_ui()
        self.update_profile_display()
        self.new_game()

    # ========================================================
    # JSON
    # ========================================================

    def load_json(self, filename, default):
        try:
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    return json.load(file)
        except Exception:
            pass

        return default

    def save_json(self, filename, data):
        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
        except Exception:
            pass

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        # ---------------- TITLE ----------------

        title = tk.Label(
            self.root,
            text="🎮 NUMBER GUESSING ARCADE",
            font=("Arial", 28, "bold"),
            bg=BG,
            fg=CYAN
        )
        title.pack(pady=(15, 5))

        subtitle = tk.Label(
            self.root,
            text="V31 • GAME MODES EDITION",
            font=("Arial", 11, "bold"),
            bg=BG,
            fg=PURPLE
        )
        subtitle.pack()

        # ---------------- TOP BAR ----------------

        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x", padx=25, pady=15)

        tk.Label(
            top,
            text="Player:",
            font=("Arial", 11, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(side="left")

        self.name_entry = tk.Entry(
            top,
            width=15,
            font=("Arial", 11),
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE
        )
        self.name_entry.pack(side="left", padx=8)

        self.name_entry.insert(0, self.profile_name)

        save_name_btn = tk.Button(
            top,
            text="Save Name",
            command=self.save_name,
            bg=PURPLE,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10
        )
        save_name_btn.pack(side="left", padx=5)

        profile_btn = tk.Button(
            top,
            text="👤 Profile",
            command=self.show_profile,
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=12
        )
        profile_btn.pack(side="right", padx=5)

        leaderboard_btn = tk.Button(
            top,
            text="🏆 Leaderboard",
            command=self.show_leaderboard,
            bg=ORANGE,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=12
        )
        leaderboard_btn.pack(side="right", padx=5)

        # ---------------- MODE PANEL ----------------

        mode_panel = tk.Frame(
            self.root,
            bg=PANEL,
            padx=15,
            pady=12
        )
        mode_panel.pack(fill="x", padx=25)

        tk.Label(
            mode_panel,
            text="GAME MODE",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=GRAY
        ).pack(side="left", padx=(0, 10))

        self.mode_var = tk.StringVar(value="Single Player")

        modes = [
            "Single Player",
            "Time Attack",
            "Survival",
            "Endless",
            "Two Player",
            "Tournament"
        ]

        self.mode_menu = tk.OptionMenu(
            mode_panel,
            self.mode_var,
            *modes,
            command=self.mode_changed
        )

        self.mode_menu.config(
            bg=PANEL2,
            fg=WHITE,
            activebackground=PURPLE,
            activeforeground=WHITE,
            font=("Arial", 10, "bold"),
            width=18
        )

        self.mode_menu["menu"].config(
            bg=PANEL2,
            fg=WHITE
        )

        self.mode_menu.pack(side="left")

        tk.Label(
            mode_panel,
            text="DIFFICULTY",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=GRAY
        ).pack(side="left", padx=(30, 10))

        self.difficulty_var = tk.StringVar(value="Medium")

        self.difficulty_menu = tk.OptionMenu(
            mode_panel,
            self.difficulty_var,
            "Easy",
            "Medium",
            "Hard",
            command=lambda x: self.new_game()
        )

        self.difficulty_menu.config(
            bg=PANEL2,
            fg=WHITE,
            activebackground=PURPLE,
            activeforeground=WHITE,
            font=("Arial", 10, "bold"),
            width=10
        )

        self.difficulty_menu["menu"].config(
            bg=PANEL2,
            fg=WHITE
        )

        self.difficulty_menu.pack(side="left")

        # ---------------- STATUS PANEL ----------------

        status = tk.Frame(
            self.root,
            bg=PANEL,
            padx=15,
            pady=12
        )
        status.pack(fill="x", padx=25, pady=12)

        self.mode_label = tk.Label(
            status,
            text="Mode: Single Player",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=CYAN
        )
        self.mode_label.pack(side="left", padx=15)

        self.attempt_label = tk.Label(
            status,
            text="Attempts: 0",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=YELLOW
        )
        self.attempt_label.pack(side="left", padx=15)

        self.timer_label = tk.Label(
            status,
            text="⏱ 00",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=GREEN
        )
        self.timer_label.pack(side="left", padx=15)

        self.score_label = tk.Label(
            status,
            text="Score: 0",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=ORANGE
        )
        self.score_label.pack(side="right", padx=15)

        self.xp_label = tk.Label(
            status,
            text="XP: 0 | Lv.1",
            font=("Arial", 11, "bold"),
            bg=PANEL,
            fg=PURPLE
        )
        self.xp_label.pack(side="right", padx=15)

        # ---------------- MAIN PANEL ----------------

        main = tk.Frame(
            self.root,
            bg=PANEL,
            padx=30,
            pady=25
        )
        main.pack(fill="both", expand=True, padx=25)

        self.instruction_label = tk.Label(
            main,
            text="Guess the hidden number!",
            font=("Arial", 20, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.instruction_label.pack(pady=10)

        self.range_label = tk.Label(
            main,
            text="Number is between 1 and 100",
            font=("Arial", 12),
            bg=PANEL,
            fg=GRAY
        )
        self.range_label.pack(pady=5)

        self.guess_entry = tk.Entry(
            main,
            font=("Arial", 22, "bold"),
            width=10,
            justify="center",
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE
        )
        self.guess_entry.pack(pady=15)

        self.guess_entry.bind(
            "<Return>",
            lambda event: self.make_guess()
        )

        self.guess_button = tk.Button(
            main,
            text="🎯 GUESS",
            command=self.make_guess,
            bg=GREEN,
            fg=BG,
            font=("Arial", 13, "bold"),
            relief="flat",
            padx=30,
            pady=8
        )
        self.guess_button.pack(pady=5)

        self.message_label = tk.Label(
            main,
            text="",
            font=("Arial", 14, "bold"),
            bg=PANEL,
            fg=WHITE,
            wraplength=800
        )
        self.message_label.pack(pady=15)

        # ---------------- POWER UPS ----------------

        power_frame = tk.Frame(main, bg=PANEL)
        power_frame.pack(pady=10)

        tk.Label(
            power_frame,
            text="POWER-UPS",
            font=("Arial", 10, "bold"),
            bg=PANEL,
            fg=GRAY
        ).pack(pady=4)

        buttons = tk.Frame(power_frame, bg=PANEL)
        buttons.pack()

        self.life_btn = tk.Button(
            buttons,
            text="❤️ Extra Life",
            command=self.use_extra_life,
            bg=RED,
            fg=WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8
        )
        self.life_btn.pack(side="left", padx=3)

        self.freeze_btn = tk.Button(
            buttons,
            text="❄️ Time Freeze",
            command=self.use_time_freeze,
            bg=CYAN,
            fg=BG,
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8
        )
        self.freeze_btn.pack(side="left", padx=3)

        self.double_btn = tk.Button(
            buttons,
            text="⭐ 2X Score",
            command=self.use_double_score,
            bg=YELLOW,
            fg=BG,
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8
        )
        self.double_btn.pack(side="left", padx=3)

        self.reveal_btn = tk.Button(
            buttons,
            text="🔍 Reveal Range",
            command=self.reveal_range,
            bg=PURPLE,
            fg=WHITE,
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8
        )
        self.reveal_btn.pack(side="left", padx=3)

        # ---------------- BOTTOM ----------------

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(fill="x", padx=25, pady=12)

        new_btn = tk.Button(
            bottom,
            text="🔄 New Game",
            command=self.new_game,
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=20
        )
        new_btn.pack(side="left")

        achievements_btn = tk.Button(
            bottom,
            text="🏅 Achievements",
            command=self.show_achievements,
            bg=PINK,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            padx=20
        )
        achievements_btn.pack(side="right")

        self.root.bind("<Escape>", lambda event: self.new_game())

    # ========================================================
    # NAME
    # ========================================================

    def save_name(self):
        name = self.name_entry.get().strip()

        if not name:
            name = "Player"

        self.player_name = name
        self.profile["name"] = name

        self.save_json(PROFILE_FILE, self.profile)

        self.message_label.config(
            text=f"Welcome, {name}! 🎮",
            fg=GREEN
        )

        self.update_profile_display()

    # ========================================================
    # MODE
    # ========================================================

    def mode_changed(self, value):
        self.mode = value
        self.new_game()

    # ========================================================
    # NEW GAME
    # ========================================================

    def new_game(self):

        self.stop_timer()

        self.mode = self.mode_var.get()
        self.difficulty = self.difficulty_var.get()

        self.power_used = False
        self.score_multiplier = 1
        self.extra_life = 0
        self.time_freeze = False

        self.player_name = self.name_entry.get().strip()

        if not self.player_name:
            self.player_name = "Player"

        self.mode_label.config(
            text=f"Mode: {self.mode}"
        )

        self.enable_powerups()

        if self.mode == "Two Player":
            self.start_two_player()

        elif self.mode == "Tournament":
            self.start_tournament()

        elif self.mode == "Time Attack":
            self.start_time_attack()

        elif self.mode == "Survival":
            self.start_survival()

        elif self.mode == "Endless":
            self.start_endless()

        else:
            self.start_single_player()

    # ========================================================
    # DIFFICULTY
    # ========================================================

    def get_difficulty_data(self):
        return self.difficulties[self.difficulty]

    # ========================================================
    # SINGLE PLAYER
    # ========================================================

    def start_single_player(self):

        data = self.get_difficulty_data()

        self.number = random.randint(1, data["max"])
        self.max_attempts = data["attempts"]
        self.attempts_left = data["attempts"]

        self.time_limit = data["time"]
        self.time_left = data["time"]

        self.score = data["score"]
        self.game_running = True

        self.range_label.config(
            text=f"Number is between 1 and {data['max']}"
        )

        self.instruction_label.config(
            text="🎯 Guess the hidden number!"
        )

        self.message_label.config(
            text="Make your first guess!",
            fg=WHITE
        )

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

        self.update_status()
        self.start_timer()

    # ========================================================
    # TIME ATTACK
    # ========================================================

    def start_time_attack(self):

        data = self.get_difficulty_data()

        self.number = random.randint(1, data["max"])

        self.max_attempts = 999
        self.attempts_left = 999

        self.time_limit = 30 if self.difficulty == "Easy" else (
            25 if self.difficulty == "Medium" else 20
        )

        self.time_left = self.time_limit

        self.time_attack_score = 0
        self.score = 0

        self.game_running = True

        self.instruction_label.config(
            text="⚡ TIME ATTACK"
        )

        self.range_label.config(
            text=f"Guess as many numbers as possible in {self.time_limit} seconds!"
        )

        self.message_label.config(
            text="Speed is everything! 🔥",
            fg=YELLOW
        )

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

        self.update_status()
        self.start_timer()

    def time_attack_next_number(self):

        data = self.get_difficulty_data()

        self.number = random.randint(1, data["max"])

        self.guess_entry.delete(0, tk.END)

        self.message_label.config(
            text="New number! Keep going! ⚡",
            fg=CYAN
        )

    # ========================================================
    # SURVIVAL
    # ========================================================

    def start_survival(self):

        self.survival_round = 1
        self.survival_lives = 3

        self.start_survival_round()

    def start_survival_round(self):

        data = self.get_difficulty_data()

        # Increase difficulty every round
        max_number = min(
            1000,
            data["max"] + (self.survival_round - 1) * 50
        )

        self.number = random.randint(1, max_number)

        self.max_attempts = max(
            3,
            data["attempts"] - (self.survival_round - 1)
        )

        self.attempts_left = self.max_attempts

        self.time_limit = max(
            15,
            data["time"] - (self.survival_round - 1) * 3
        )

        self.time_left = self.time_limit

        self.score = self.survival_round * 100
        self.game_running = True

        self.instruction_label.config(
            text=f"💀 SURVIVAL — ROUND {self.survival_round}"
        )

        self.range_label.config(
            text=f"Number is between 1 and {max_number}"
        )

        self.message_label.config(
            text=f"❤️ Lives: {self.survival_lives}",
            fg=RED
        )

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

        self.update_status()
        self.start_timer()

    # ========================================================
    # ENDLESS
    # ========================================================

    def start_endless(self):

        self.endless_round = 1
        self.endless_lives = 3

        self.start_endless_round()

    def start_endless_round(self):

        data = self.get_difficulty_data()

        max_number = min(
            2000,
            data["max"] + (self.endless_round - 1) * 25
        )

        self.number = random.randint(1, max_number)

        self.max_attempts = max(
            3,
            data["attempts"] - (self.endless_round // 3)
        )

        self.attempts_left = self.max_attempts

        self.time_limit = max(
            10,
            data["time"] - (self.endless_round // 2)
        )

        self.time_left = self.time_limit

        self.score = self.endless_round * 75

        self.game_running = True

        self.instruction_label.config(
            text=f"♾️ ENDLESS — ROUND {self.endless_round}"
        )

        self.range_label.config(
            text=f"Number is between 1 and {max_number}"
        )

        self.message_label.config(
            text=f"❤️ Lives: {self.endless_lives}",
            fg=CYAN
        )

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

        self.update_status()
        self.start_timer()

    # ========================================================
    # TWO PLAYER
    # ========================================================

    def start_two_player(self):

        self.player1_score = 0
        self.player2_score = 0

        self.current_turn = 1

        self.start_competitive_round()

    # ========================================================
    # TOURNAMENT
    # ========================================================

    def start_tournament(self):

        self.player1_score = 0
        self.player2_score = 0

        self.tournament_round = 1
        self.current_turn = 1

        self.start_competitive_round()

    # ========================================================
    # COMPETITIVE ROUND
    # ========================================================

    def start_competitive_round(self):

        data = self.get_difficulty_data()

        self.number = random.randint(1, data["max"])

        self.max_attempts = data["attempts"]
        self.attempts_left = data["attempts"]

        self.time_limit = data["time"]
        self.time_left = data["time"]

        self.score = data["score"]

        self.game_running = True

        if self.mode == "Tournament":
            prefix = (
                f"🏆 TOURNAMENT — ROUND "
                f"{self.tournament_round}/{self.total_rounds}"
            )
        else:
            prefix = "⚔️ TWO PLAYER"

        player = (
            "Player 1"
            if self.current_turn == 1
            else "Player 2"
        )

        self.instruction_label.config(
            text=f"{prefix} • {player}"
        )

        self.range_label.config(
            text=f"Number is between 1 and {data['max']}"
        )

        self.message_label.config(
            text=f"{player}'s turn!",
            fg=CYAN
        )

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

        self.update_status()
        self.start_timer()

    # ========================================================
    # GUESS
    # ========================================================

    def make_guess(self):

        if not self.game_running:
            return

        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.message_label.config(
                text="❌ Enter a valid number!",
                fg=RED
            )
            return

        self.profile["total_guesses"] = (
            self.profile.get("total_guesses", 0) + 1
        )

        # ---------------- TIME ATTACK ----------------

        if self.mode == "Time Attack":

            if guess == self.number:

                gained = max(
                    10,
                    self.time_left * 2
                )

                gained *= self.score_multiplier

                self.time_attack_score += gained
                self.score = self.time_attack_score

                self.message_label.config(
                    text=f"🔥 CORRECT! +{gained} points!",
                    fg=GREEN
                )

                self.time_attack_next_number()

            else:

                if guess < self.number:
                    hint = "⬆️ Higher!"
                else:
                    hint = "⬇️ Lower!"

                self.message_label.config(
                    text=hint,
                    fg=ORANGE
                )

            self.update_status()
            return

        # ---------------- NORMAL GUESS ----------------

        self.attempts_left -= 1

        if guess == self.number:

            self.handle_correct_guess()

        else:

            if guess < self.number:
                self.message_label.config(
                    text="⬆️ Too low!",
                    fg=CYAN
                )
            else:
                self.message_label.config(
                    text="⬇️ Too high!",
                    fg=ORANGE
                )

            if self.mode == "Survival":
                if self.attempts_left <= 0:
                    self.survival_life_lost()
                    return

            elif self.mode == "Endless":
                if self.attempts_left <= 0:
                    self.endless_life_lost()
                    return

            elif self.attempts_left <= 0:
                self.handle_loss()
                return

        self.update_status()

    # ========================================================
    # CORRECT GUESS
    # ========================================================

    def handle_correct_guess(self):

        self.stop_timer()

        if self.mode == "Single Player":

            gained = max(
                50,
                self.score + self.attempts_left * 10 + self.time_left
            )

            gained *= self.score_multiplier

            self.score = gained

            self.streak += 1
            self.combo = min(5, self.combo + 1)

            self.profile["games"] += 1
            self.profile["wins"] += 1

            self.stats[self.difficulty]["games"] += 1
            self.stats[self.difficulty]["wins"] += 1

            self.add_xp(100 + self.streak * 20)

            if self.score > self.profile["highest_score"]:
                self.profile["highest_score"] = self.score

            if self.streak > self.profile["best_streak"]:
                self.profile["best_streak"] = self.streak

            self.save_profile_data()
            self.check_achievements()

            self.add_leaderboard_score()

            self.game_running = False

            self.message_label.config(
                text=(
                    f"🎉 CORRECT! The number was {self.number}!\n"
                    f"🏆 Score: {self.score}\n"
                    f"🔥 Streak: {self.streak}"
                ),
                fg=GREEN
            )

            self.update_status()

        elif self.mode == "Survival":

            self.survival_round += 1

            self.add_xp(50)

            self.message_label.config(
                text=(
                    f"🔥 ROUND CLEARED!\n"
                    f"Next round: {self.survival_round}"
                ),
                fg=GREEN
            )

            self.root.after(
                1200,
                self.start_survival_round
            )

        elif self.mode == "Endless":

            self.endless_round += 1

            self.add_xp(40)

            self.message_label.config(
                text=(
                    f"♾️ ROUND {self.endless_round - 1} CLEARED!\n"
                    f"Keep going!"
                ),
                fg=GREEN
            )

            self.root.after(
                1000,
                self.start_endless_round
            )

        else:

            self.handle_competitive_win()

    # ========================================================
    # SURVIVAL LIFE
    # ========================================================

    def survival_life_lost(self):

        self.stop_timer()

        self.survival_lives -= 1

        if self.survival_lives <= 0:

            self.game_running = False

            self.message_label.config(
                text=(
                    f"💀 SURVIVAL OVER!\n"
                    f"You reached Round {self.survival_round}"
                ),
                fg=RED
            )

            self.profile["games"] += 1
            self.profile["losses"] += 1

            self.save_profile_data()

        else:

            self.message_label.config(
                text=(
                    f"💔 Life lost!\n"
                    f"❤️ Lives remaining: {self.survival_lives}"
                ),
                fg=RED
            )

            self.root.after(
                1200,
                self.start_survival_round
            )

    # ========================================================
    # ENDLESS LIFE
    # ========================================================

    def endless_life_lost(self):

        self.stop_timer()

        self.endless_lives -= 1

        if self.endless_lives <= 0:

            self.game_running = False

            self.message_label.config(
                text=(
                    f"♾️ ENDLESS RUN OVER!\n"
                    f"Rounds survived: {self.endless_round - 1}"
                ),
                fg=RED
            )

            self.profile["games"] += 1
            self.profile["losses"] += 1

            self.save_profile_data()

        else:

            self.message_label.config(
                text=(
                    f"💔 Life lost!\n"
                    f"❤️ Lives remaining: {self.endless_lives}"
                ),
                fg=RED
            )

            self.root.after(
                1200,
                self.start_endless_round
            )

    # ========================================================
    # COMPETITIVE WIN
    # ========================================================

    def handle_competitive_win(self):

        points = max(
            50,
            self.score + self.attempts_left * 10 + self.time_left
        )

        player = (
            "Player 1"
            if self.current_turn == 1
            else "Player 2"
        )

        if self.current_turn == 1:
            self.player1_score += points
        else:
            self.player2_score += points

        if self.mode == "Two Player":

            if self.current_turn == 1:

                self.current_turn = 2

                self.message_label.config(
                    text=(
                        f"🎯 Player 1 scored {points}!\n"
                        f"Now Player 2's turn."
                    ),
                    fg=GREEN
                )

                self.root.after(
                    1300,
                    self.start_competitive_round
                )

            else:

                self.game_running = False

                self.show_competitive_result()

        else:

            if self.current_turn == 1:

                self.current_turn = 2

                self.message_label.config(
                    text=(
                        f"🎯 Player 1 scored {points}!\n"
                        f"Player 2's turn!"
                    ),
                    fg=GREEN
                )

                self.root.after(
                    1300,
                    self.start_competitive_round
                )

            else:

                self.finish_tournament_round()

    # ========================================================
    # TOURNAMENT ROUND
    # ========================================================

    def finish_tournament_round(self):

        self.game_running = False

        p1 = self.player1_score
        p2 = self.player2_score

        if self.tournament_round >= self.total_rounds:

            self.show_tournament_result()

        else:

            self.tournament_round += 1
            self.current_turn = 1

            self.message_label.config(
                text=(
                    f"🏆 Round {self.tournament_round - 1} complete!\n"
                    f"Player 1: {p1}   |   Player 2: {p2}"
                ),
                fg=YELLOW
            )

            self.root.after(
                1800,
                self.start_competitive_round
            )

    # ========================================================
    # RESULTS
    # ========================================================

    def show_competitive_result(self):

        self.stop_timer()

        if self.player1_score > self.player2_score:

            result = (
                f"🏆 PLAYER 1 WINS!\n\n"
                f"Player 1: {self.player1_score}\n"
                f"Player 2: {self.player2_score}"
            )

        elif self.player2_score > self.player1_score:

            result = (
                f"🏆 PLAYER 2 WINS!\n\n"
                f"Player 1: {self.player1_score}\n"
                f"Player 2: {self.player2_score}"
            )

        else:

            result = (
                f"🤝 DRAW!\n\n"
                f"Player 1: {self.player1_score}\n"
                f"Player 2: {self.player2_score}"
            )

        self.message_label.config(
            text=result,
            fg=YELLOW
        )

    def show_tournament_result(self):

        self.stop_timer()

        if self.player1_score > self.player2_score:

            result = (
                "🏆 TOURNAMENT CHAMPION: PLAYER 1!\n\n"
                f"Player 1: {self.player1_score}\n"
                f"Player 2: {self.player2_score}"
            )

        elif self.player2_score > self.player1_score:

            result = (
                "🏆 TOURNAMENT CHAMPION: PLAYER 2!\n\n"
                f"Player 1: {self.player1_score}\n"
                f"Player 2: {self.player2_score}"
            )

        else:

            result = (
                "🤝 TOURNAMENT DRAW!\n\n"
                f"Player 1: {self.player1_score}\n"
                f"Player 2: {self.player2_score}"
            )

        self.game_running = False

        self.message_label.config(
            text=result,
            fg=YELLOW
        )

    # ========================================================
    # LOSS
    # ========================================================

    def handle_loss(self):

        self.stop_timer()

        self.game_running = False

        self.profile["games"] += 1
        self.profile["losses"] += 1

        self.streak = 0
        self.combo = 1

        self.save_profile_data()

        self.message_label.config(
            text=(
                f"💀 GAME OVER!\n"
                f"The number was {self.number}"
            ),
            fg=RED
        )

        self.update_status()

    # ========================================================
    # TIMER
    # ========================================================

    def start_timer(self):

        self.stop_timer()

        self.timer_tick()

    def timer_tick(self):

        if not self.game_running:
            return

        if self.time_freeze:
            self.timer_id = self.root.after(
                1000,
                self.timer_tick
            )
            return

        self.time_left -= 1

        self.update_status()

        if self.time_left <= 0:

            self.time_left = 0

            if self.mode == "Time Attack":

                self.game_running = False

                self.message_label.config(
                    text=(
                        f"⏰ TIME'S UP!\n"
                        f"Final Score: {self.time_attack_score}"
                    ),
                    fg=RED
                )

                self.add_xp(self.time_attack_score // 10)

            elif self.mode == "Survival":

                self.survival_life_lost()

            elif self.mode == "Endless":

                self.endless_life_lost()

            else:

                self.handle_loss()

            return

        self.timer_id = self.root.after(
            1000,
            self.timer_tick
        )

    def stop_timer(self):

        if self.timer_id is not None:

            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass

            self.timer_id = None

    # ========================================================
    # POWER UPS
    # ========================================================

    def competitive_powerup_blocked(self):

        return self.mode in [
            "Two Player",
            "Tournament"
        ]

    def use_extra_life(self):

        if not self.game_running:
            return

        if self.competitive_powerup_blocked():
            return

        if self.power_used:
            return

        self.power_used = True
        self.extra_life += 2

        self.attempts_left += 2

        self.message_label.config(
            text="❤️ EXTRA LIFE ACTIVATED! +2 attempts",
            fg=RED
        )

        self.disable_powerups()

        self.update_status()

    def use_time_freeze(self):

        if not self.game_running:
            return

        if self.competitive_powerup_blocked():
            return

        if self.power_used:
            return

        self.power_used = True
        self.time_freeze = True

        self.message_label.config(
            text="❄️ TIME FROZEN FOR 10 SECONDS!",
            fg=CYAN
        )

        self.disable_powerups()

        self.root.after(
            10000,
            self.end_time_freeze
        )

    def end_time_freeze(self):

        self.time_freeze = False

    def use_double_score(self):

        if not self.game_running:
            return

        if self.competitive_powerup_blocked():
            return

        if self.power_used:
            return

        self.power_used = True
        self.score_multiplier = 2

        self.message_label.config(
            text="⭐ 2X SCORE ACTIVATED!",
            fg=YELLOW
        )

        self.disable_powerups()

    def reveal_range(self):

        if not self.game_running:
            return

        if self.competitive_powerup_blocked():
            return

        if self.power_used:
            return

        self.power_used = True

        low = max(1, self.number - 10)
        high = self.number + 10

        self.range_label.config(
            text=f"🔍 Secret range: {low} - {high}"
        )

        self.message_label.config(
            text="🔍 Range revealed!",
            fg=PURPLE
        )

        self.disable_powerups()

    def disable_powerups(self):

        for button in [
            self.life_btn,
            self.freeze_btn,
            self.double_btn,
            self.reveal_btn
        ]:
            button.config(
                state="disabled"
            )

    def enable_powerups(self):

        for button in [
            self.life_btn,
            self.freeze_btn,
            self.double_btn,
            self.reveal_btn
        ]:
            button.config(
                state="normal"
            )

    # ========================================================
    # XP / LEVEL
    # ========================================================

    def add_xp(self, amount):

        self.profile["xp"] = self.profile.get(
            "xp",
            0
        ) + amount

        self.update_level()

        self.save_profile_data()

    def update_level(self):

        xp = self.profile.get("xp", 0)

        new_level = max(
            1,
            xp // 500 + 1
        )

        old_level = self.profile.get(
            "level",
            1
        )

        self.profile["level"] = new_level

        if new_level > old_level:

            self.message_label.config(
                text=f"🎉 LEVEL UP! You are now Level {new_level}!",
                fg=PURPLE
            )

        self.update_profile_display()

    # ========================================================
    # PROFILE
    # ========================================================

    def save_profile_data(self):

        self.save_json(
            PROFILE_FILE,
            self.profile
        )

        self.save_json(
            STATS_FILE,
            self.stats
        )

        self.update_profile_display()

    def update_profile_display(self):

        xp = self.profile.get("xp", 0)
        level = self.profile.get("level", 1)

        self.xp_label.config(
            text=f"XP: {xp} | Lv.{level}"
        )

    # ========================================================
    # LEADERBOARD
    # ========================================================

    def add_leaderboard_score(self):

        leaderboard = self.load_json(
            LEADERBOARD_FILE,
            []
        )

        leaderboard.append(
            {
                "name": self.player_name,
                "score": self.score,
                "mode": self.mode,
                "difficulty": self.difficulty
            }
        )

        leaderboard.sort(
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        leaderboard = leaderboard[:10]

        self.save_json(
            LEADERBOARD_FILE,
            leaderboard
        )

    def show_leaderboard(self):

        leaderboard = self.load_json(
            LEADERBOARD_FILE,
            []
        )

        window = tk.Toplevel(self.root)
        window.title("🏆 Leaderboard")
        window.geometry("600x500")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="🏆 TOP 10 LEADERBOARD",
            font=("Arial", 20, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(pady=20)

        if not leaderboard:

            tk.Label(
                window,
                text="No scores yet!",
                font=("Arial", 14),
                bg=BG,
                fg=GRAY
            ).pack()

        else:

            for i, entry in enumerate(
                leaderboard,
                start=1
            ):

                text = (
                    f"{i}. {entry.get('name', 'Player')}   "
                    f"• {entry.get('score', 0)} pts   "
                    f"• {entry.get('mode', 'Unknown')}"
                )

                tk.Label(
                    window,
                    text=text,
                    font=("Arial", 11, "bold"),
                    bg=PANEL,
                    fg=WHITE,
                    anchor="w",
                    padx=15,
                    pady=8
                ).pack(
                    fill="x",
                    padx=25,
                    pady=3
                )

    # ========================================================
    # PROFILE WINDOW
    # ========================================================

    def show_profile(self):

        window = tk.Toplevel(self.root)
        window.title("👤 Player Profile")
        window.geometry("600x600")
        window.configure(bg=BG)

        name = self.profile.get(
            "name",
            "Player"
        )

        games = self.profile.get(
            "games",
            0
        )

        wins = self.profile.get(
            "wins",
            0
        )

        losses = self.profile.get(
            "losses",
            0
        )

        win_rate = (
            (wins / games) * 100
            if games > 0
            else 0
        )

        highest = self.profile.get(
            "highest_score",
            0
        )

        best_streak = self.profile.get(
            "best_streak",
            0
        )

        total_guesses = self.profile.get(
            "total_guesses",
            0
        )

        achievements = len(
            self.achievements
        )

        stats = [
            ("👤 Player", name),
            ("⭐ Level", self.profile.get("level", 1)),
            ("✨ XP", self.profile.get("xp", 0)),
            ("🎮 Games", games),
            ("🏆 Wins", wins),
            ("💀 Losses", losses),
            ("📈 Win Rate", f"{win_rate:.1f}%"),
            ("🔥 Best Streak", best_streak),
            ("💰 Highest Score", highest),
            ("🎯 Total Guesses", total_guesses),
            ("🏅 Achievements", achievements)
        ]

        tk.Label(
            window,
            text="👤 PLAYER PROFILE",
            font=("Arial", 22, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=20)

        for label, value in stats:

            row = tk.Frame(
                window,
                bg=PANEL
            )
            row.pack(
                fill="x",
                padx=50,
                pady=4
            )

            tk.Label(
                row,
                text=str(label),
                font=("Arial", 11, "bold"),
                bg=PANEL,
                fg=GRAY,
                width=20,
                anchor="w"
            ).pack(
                side="left",
                padx=10,
                pady=8
            )

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 11, "bold"),
                bg=PANEL,
                fg=WHITE
            ).pack(
                side="right",
                padx=10
            )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    def check_achievements(self):

        achievements = {
            "first_win": (
                self.profile.get("wins", 0) >= 1,
                "🏆 First Win"
            ),

            "sharp_shooter": (
                self.attempts_left >= 7,
                "🎯 Sharp Shooter"
            ),

            "on_fire": (
                self.streak >= 3,
                "🔥 On Fire"
            ),

            "power_player": (
                self.power_used,
                "💥 Power Player"
            ),

            "high_roller": (
                self.score >= 500,
                "💰 High Roller"
            ),

            "no_help": (
                not self.power_used,
                "🧠 No Help Needed"
            ),

            "speed_demon": (
                self.time_left >= 30,
                "⚡ Speed Demon"
            ),

            "hard_mode": (
                self.difficulty == "Hard",
                "💀 Hard Mode"
            ),

            "five_streak": (
                self.streak >= 5,
                "🔥 Five Streak"
            ),

            "level_five": (
                self.profile.get("level", 1) >= 5,
                "⭐ Level Five"
            )
        }

        for key, (condition, name) in achievements.items():

            if condition and key not in self.achievements:

                self.achievements[key] = {
                    "name": name,
                    "unlocked": True
                }

                self.save_json(
                    ACHIEVEMENTS_FILE,
                    self.achievements
                )

    def show_achievements(self):

        window = tk.Toplevel(self.root)
        window.title("🏅 Achievements")
        window.geometry("600x600")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="🏅 ACHIEVEMENT HALL",
            font=("Arial", 22, "bold"),
            bg=BG,
            fg=PINK
        ).pack(pady=20)

        all_achievements = [
            ("first_win", "🏆 First Win"),
            ("sharp_shooter", "🎯 Sharp Shooter"),
            ("on_fire", "🔥 On Fire"),
            ("power_player", "💥 Power Player"),
            ("high_roller", "💰 High Roller"),
            ("no_help", "🧠 No Help Needed"),
            ("speed_demon", "⚡ Speed Demon"),
            ("hard_mode", "💀 Hard Mode"),
            ("five_streak", "🔥 Five Streak"),
            ("level_five", "⭐ Level Five")
        ]

        for key, name in all_achievements:

            unlocked = key in self.achievements

            text = (
                f"✅ {name}"
                if unlocked
                else f"🔒 {name}"
            )

            color = (
                GREEN
                if unlocked
                else GRAY
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 12, "bold"),
                bg=PANEL,
                fg=color,
                anchor="w",
                padx=20,
                pady=10
            ).pack(
                fill="x",
                padx=40,
                pady=3
            )

    # ========================================================
    # STATUS
    # ========================================================

    def update_status(self):

        self.attempt_label.config(
            text=f"Attempts: {self.attempts_left}"
        )

        self.timer_label.config(
            text=f"⏱ {self.time_left:02d}"
        )

        if self.mode == "Time Attack":

            self.score_label.config(
                text=f"Score: {self.time_attack_score}"
            )

        elif self.mode in [
            "Two Player",
            "Tournament"
        ]:

            self.score_label.config(
                text=(
                    f"P1: {self.player1_score} "
                    f"| P2: {self.player2_score}"
                )
            )

        else:

            self.score_label.config(
                text=f"Score: {self.score}"
            )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = NumberGuessingGame(root)

    root.mainloop()