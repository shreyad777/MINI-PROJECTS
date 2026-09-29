import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

# ============================================================
# NUMBER GUESSING GAME V29
# PLAYER PROFILE & STATISTICS EDITION
# ============================================================

SAVE_FILE = "leaderboard_v29.json"
PROFILE_FILE = "player_profile_v29.json"
ACHIEVEMENT_FILE = "achievements_v29.json"
STATS_FILE = "game_statistics_v29.json"

# ---------------- COLORS ----------------

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

# ---------------- DIFFICULTY ----------------

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

# ---------------- QUESTS ----------------

QUESTS = [
    ("First Strike", "Win a game", 100),
    ("Sharp Shooter", "Win within 3 guesses", 125),
    ("Hot Streak", "Get a 3-win streak", 150),
    ("Power Player", "Use a power-up and win", 125),
    ("Speed Demon", "Win with 10+ seconds remaining", 150),
    ("High Roller", "Score 300+", 150),
    ("Hintless Hero", "Win without using a hint", 150)
]

# ---------------- ACHIEVEMENTS ----------------

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
        "description": "Win without using a hint",
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
        "description": "Win on Hard difficulty",
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
            with open(filename, "r", encoding="utf-8") as file:
                return json.load(file)
    except Exception:
        pass

    return default


def save_json(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except Exception:
        pass


# ============================================================
# MAIN GAME
# ============================================================

class NumberGuessingGame:

    def __init__(self, root):

        self.root = root
        self.root.title("Number Guessing Game V29")
        self.root.geometry("1250x760")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ---------------- PLAYER ----------------

        self.player_name = "Player"

        # ---------------- PROFILE ----------------

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

        # ---------------- STATISTICS ----------------

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

        # ---------------- ACHIEVEMENTS ----------------

        self.achievements = load_json(
            ACHIEVEMENT_FILE,
            {}
        )

        # ---------------- LEADERBOARD ----------------

        self.leaderboard = load_json(
            SAVE_FILE,
            []
        )

        # ---------------- GAME STATE ----------------

        self.secret_number = 0
        self.attempts_left = 0
        self.current_score = 0
        self.start_time = 0
        self.time_left = 0
        self.timer_running = False

        self.streak = 0
        self.combo = 1

        self.hints_left = 2
        self.used_hint = False

        self.extra_life = True
        self.time_freeze = True
        self.double_score = True
        self.reveal_range = True

        self.power_used = False

        self.current_difficulty = "Easy"

        self.active_quests = random.sample(QUESTS, 3)
        self.completed_quests = []

        self.mode = "Single Player"

        # ---------------- UI ----------------

        self.build_ui()
        self.new_game()

    # ========================================================
    # UI
    # ========================================================

    def build_ui(self):

        # ---------------- TITLE ----------------

        title = tk.Label(
            self.root,
            text="🎯 NUMBER GUESSING ARCADE",
            font=("Segoe UI", 26, "bold"),
            bg=BG,
            fg=CYAN
        )
        title.pack(pady=(15, 2))

        subtitle = tk.Label(
            self.root,
            text="V29 • PLAYER PROFILE & STATISTICS EDITION",
            font=("Segoe UI", 10, "bold"),
            bg=BG,
            fg=PURPLE
        )
        subtitle.pack()

        # ---------------- MAIN AREA ----------------

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=18, pady=15)

        # ====================================================
        # LEFT PANEL
        # ====================================================

        left = tk.Frame(
            main,
            bg=PANEL,
            width=250,
            height=620
        )
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        tk.Label(
            left,
            text="⚙ GAME SETTINGS",
            font=("Segoe UI", 14, "bold"),
            bg=PANEL,
            fg=WHITE
        ).pack(pady=18)

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
        self.name_entry.insert(0, self.player_name)
        self.name_entry.pack(pady=7, padx=25, fill="x")

        tk.Label(
            left,
            text="Difficulty",
            bg=PANEL,
            fg=GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(15, 3))

        self.difficulty_var = tk.StringVar(value="Easy")

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
            ).pack(anchor="w", padx=35)

        tk.Label(
            left,
            text="Game Mode",
            bg=PANEL,
            fg=GRAY,
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(18, 3))

        self.mode_var = tk.StringVar(value="Single Player")

        for mode in ["Single Player", "Two Player", "Tournament"]:

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
            ).pack(anchor="w", padx=35)

        tk.Button(
            left,
            text="👤 PLAYER PROFILE",
            command=self.show_profile,
            bg=PURPLE,
            fg=WHITE,
            activebackground=BLUE,
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(pady=(20, 7), padx=25, fill="x")

        tk.Button(
            left,
            text="🏆 LEADERBOARD",
            command=self.show_leaderboard,
            bg=BLUE,
            fg=WHITE,
            activebackground=CYAN,
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(pady=5, padx=25, fill="x")

        tk.Button(
            left,
            text="🎖 ACHIEVEMENTS",
            command=self.show_achievements,
            bg=ORANGE,
            fg=WHITE,
            activebackground=YELLOW,
            activeforeground=BG,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(pady=5, padx=25, fill="x")

        # ====================================================
        # CENTER PANEL
        # ====================================================

        center = tk.Frame(
            main,
            bg=PANEL,
            width=600,
            height=620
        )
        center.pack(side="left", fill="both", expand=True, padx=10)
        center.pack_propagate(False)

        # STATUS

        self.status_label = tk.Label(
            center,
            text="Guess the secret number!",
            font=("Segoe UI", 15, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.status_label.pack(pady=(20, 12))

        # TIMER

        self.timer_label = tk.Label(
            center,
            text="⏱ 00:00",
            font=("Segoe UI", 18, "bold"),
            bg=PANEL,
            fg=YELLOW
        )
        self.timer_label.pack()

        # SCORE

        self.score_label = tk.Label(
            center,
            text="⭐ Score: 0",
            font=("Segoe UI", 13, "bold"),
            bg=PANEL,
            fg=GREEN
        )
        self.score_label.pack(pady=8)

        # STREAK

        self.streak_label = tk.Label(
            center,
            text="🔥 Streak: 0   Combo: x1",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL,
            fg=ORANGE
        )
        self.streak_label.pack()

        # RANGE

        self.range_label = tk.Label(
            center,
            text="",
            font=("Segoe UI", 12),
            bg=PANEL,
            fg=CYAN
        )
        self.range_label.pack(pady=20)

        # GUESS ENTRY

        self.guess_entry = tk.Entry(
            center,
            font=("Segoe UI", 22, "bold"),
            bg=PANEL2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            justify="center"
        )
        self.guess_entry.pack(padx=100, fill="x", ipady=8)
        self.guess_entry.bind("<Return>", lambda event: self.check_guess())

        tk.Button(
            center,
            text="🎯 MAKE GUESS",
            command=self.check_guess,
            bg=GREEN,
            fg=BG,
            activebackground=CYAN,
            activeforeground=BG,
            relief="flat",
            font=("Segoe UI", 13, "bold"),
            cursor="hand2"
        ).pack(pady=15, ipadx=20, ipady=6)

        # ATTEMPTS

        self.attempts_label = tk.Label(
            center,
            text="Attempts: 0",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=WHITE
        )
        self.attempts_label.pack(pady=5)

        # POWER UPS

        power_frame = tk.Frame(center, bg=PANEL)
        power_frame.pack(pady=12)

        tk.Label(
            power_frame,
            text="⚡ POWER-UPS",
            font=("Segoe UI", 11, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack()

        buttons = tk.Frame(power_frame, bg=PANEL)
        buttons.pack(pady=8)

        self.life_button = tk.Button(
            buttons,
            text="❤️ +2 LIFE",
            command=self.use_extra_life,
            bg=RED,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        self.life_button.pack(side="left", padx=4)

        self.freeze_button = tk.Button(
            buttons,
            text="❄️ FREEZE",
            command=self.use_time_freeze,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        self.freeze_button.pack(side="left", padx=4)

        self.double_button = tk.Button(
            buttons,
            text="⭐ 2X SCORE",
            command=self.use_double_score,
            bg=YELLOW,
            fg=BG,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        self.double_button.pack(side="left", padx=4)

        self.range_button = tk.Button(
            buttons,
            text="🔍 RANGE",
            command=self.use_reveal_range,
            bg=PURPLE,
            fg=WHITE,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        self.range_button.pack(side="left", padx=4)

        # NEW GAME

        tk.Button(
            center,
            text="🔄 NEW GAME",
            command=self.new_game,
            bg=PANEL2,
            fg=WHITE,
            activebackground=PURPLE,
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        ).pack(pady=8)

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right = tk.Frame(
            main,
            bg=PANEL,
            width=260,
            height=620
        )
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        tk.Label(
            right,
            text="👤 PLAYER",
            font=("Segoe UI", 14, "bold"),
            bg=PANEL,
            fg=CYAN
        ).pack(pady=(18, 5))

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
        self.level_display.pack(pady=5)

        # XP

        self.xp_label = tk.Label(
            right,
            text="XP: 0",
            font=("Segoe UI", 10, "bold"),
            bg=PANEL,
            fg=GREEN
        )
        self.xp_label.pack(pady=(10, 2))

        self.xp_bar = tk.Canvas(
            right,
            width=210,
            height=16,
            bg=PANEL2,
            highlightthickness=0
        )
        self.xp_bar.pack(pady=3)

        # QUICK STATS

        tk.Label(
            right,
            text="📊 QUICK STATS",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL,
            fg=PURPLE
        ).pack(pady=(20, 10))

        self.quick_stats = tk.Label(
            right,
            text="",
            justify="left",
            anchor="w",
            font=("Segoe UI", 10),
            bg=PANEL,
            fg=WHITE
        )
        self.quick_stats.pack(padx=20, fill="x")

        # QUESTS

        tk.Label(
            right,
            text="🎯 ACTIVE QUESTS",
            font=("Segoe UI", 12, "bold"),
            bg=PANEL,
            fg=ORANGE
        ).pack(pady=(25, 10))

        self.quest_label = tk.Label(
            right,
            text="",
            justify="left",
            anchor="w",
            font=("Segoe UI", 9),
            bg=PANEL,
            fg=WHITE
        )
        self.quest_label.pack(padx=15, fill="x")

        self.update_profile_display()

    # ========================================================
    # GAME FUNCTIONS
    # ========================================================

    def change_mode(self):

        self.mode = self.mode_var.get()

        if self.mode == "Two Player":
            messagebox.showinfo(
                "Two Player Mode",
                "Two Player Mode is selected.\n\n"
                "The full competitive mode will be expanded in V30!"
            )

        elif self.mode == "Tournament":
            messagebox.showinfo(
                "Tournament Mode",
                "Tournament Mode is selected.\n\n"
                "The full tournament system will be expanded in V30!"
            )

        self.new_game()

    def new_game(self):

        self.player_name = self.name_entry.get().strip()

        if not self.player_name:
            self.player_name = "Player"

        self.player_display.config(
            text=self.player_name
        )

        self.current_difficulty = self.difficulty_var.get()

        difficulty = DIFFICULTIES[
            self.current_difficulty
        ]

        self.secret_number = random.randint(
            1,
            difficulty["max"]
        )

        self.attempts_left = difficulty["attempts"]

        self.current_score = difficulty["score"]

        self.time_left = difficulty["time"]

        self.start_time = time.time()

        self.timer_running = True

        self.hints_left = 2
        self.used_hint = False

        self.power_used = False

        self.extra_life = True
        self.time_freeze = True
        self.double_score = True
        self.reveal_range = True

        self.life_button.config(state="normal")
        self.freeze_button.config(state="normal")
        self.double_button.config(state="normal")
        self.range_button.config(state="normal")

        self.guess_entry.delete(0, tk.END)

        self.status_label.config(
            text="🎯 Guess the secret number!"
        )

        self.range_label.config(
            text=f"Number is between 1 and {difficulty['max']}"
        )

        self.update_game_display()

        self.timer_tick()

    def timer_tick(self):

        if not self.timer_running:
            return

        if self.time_left <= 0:

            self.timer_running = False

            self.end_game(False, "⏰ Time's up!")

            return

        self.timer_label.config(
            text=f"⏱ {self.time_left:02d}s"
        )

        self.time_left -= 1

        self.root.after(1000, self.timer_tick)

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
        self.statistics["total_guesses"] += 1

        if guess == self.secret_number:

            self.timer_running = False

            guesses_used = (
                DIFFICULTIES[self.current_difficulty]["attempts"]
                - self.attempts_left
            )

            self.handle_win(guesses_used)

            return

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

            self.end_game(
                False,
                f"💥 Out of attempts!\n"
                f"The number was {self.secret_number}."
            )

            return

        self.update_game_display()

    # ========================================================
    # WIN
    # ========================================================

    def handle_win(self, guesses_used):

        self.profile["total_games"] += 1
        self.profile["total_wins"] += 1

        self.streak += 1

        if self.streak > self.profile["best_streak"]:
            self.profile["best_streak"] = self.streak

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

        self.statistics["highest_score"] = max(
            self.statistics["highest_score"],
            score
        )

        self.statistics["difficulty"][
            self.current_difficulty
        ]["games"] += 1

        self.statistics["difficulty"][
            self.current_difficulty
        ]["wins"] += 1

        self.statistics["difficulty"][
            self.current_difficulty
        ]["score"] += score

        self.add_xp(100)

        self.check_achievements(
            guesses_used
        )

        self.check_quests(
            guesses_used
        )

        self.save_all()

        self.update_profile_display()

        messagebox.showinfo(
            "🎉 YOU WIN!",
            f"Congratulations {self.player_name}!\n\n"
            f"Secret Number: {self.secret_number}\n"
            f"Guesses Used: {guesses_used}\n"
            f"Score: {score}\n"
            f"Streak: {self.streak}\n"
            f"Combo: x{self.combo}"
        )

        self.timer_running = False

        self.record_leaderboard()

    # ========================================================
    # LOSS
    # ========================================================

    def end_game(self, won, message):

        if not won:

            self.profile["total_games"] += 1

            self.streak = 0
            self.combo = 1

            self.statistics["difficulty"][
                self.current_difficulty
            ]["games"] += 1

            self.save_all()

            self.update_profile_display()

        messagebox.showinfo(
            "Game Over",
            message
        )

    # ========================================================
    # POWER UPS
    # ========================================================

    def use_extra_life(self):

        if not self.extra_life:
            return

        self.extra_life = False

        self.attempts_left += 2

        self.power_used = True

        self.life_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="❤️ +2 Attempts!"
        )

        self.update_game_display()

    def use_time_freeze(self):

        if not self.time_freeze:
            return

        self.time_freeze = False

        self.power_used = True

        self.freeze_button.config(
            state="disabled"
        )

        self.timer_running = False

        self.status_label.config(
            text="❄️ Time Frozen for 10 seconds!"
        )

        self.root.after(
            10000,
            self.resume_timer
        )

    def resume_timer(self):

        if self.timer_running:
            return

        self.timer_running = True
        self.timer_tick()

    def use_double_score(self):

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

        upper = self.secret_number + 10

        maximum = DIFFICULTIES[
            self.current_difficulty
        ]["max"]

        upper = min(
            maximum,
            upper
        )

        self.range_label.config(
            text=f"🔍 Secret is between {lower} and {upper}"
        )

    # ========================================================
    # XP
    # ========================================================

    def add_xp(self, amount):

        self.profile["xp"] += amount

        self.statistics["total_xp_earned"] += amount

        while self.profile["xp"] >= (
            self.profile["level"] * 250
        ):

            required = self.profile["level"] * 250

            self.profile["xp"] -= required

            self.profile["level"] += 1

            self.statistics["highest_level"] = max(
                self.statistics["highest_level"],
                self.profile["level"]
            )

            messagebox.showinfo(
                "⭐ LEVEL UP!",
                f"Congratulations!\n\n"
                f"You reached Level "
                f"{self.profile['level']}!"
            )

    # ========================================================
    # ACHIEVEMENTS
    # ========================================================

    def unlock_achievement(self, key):

        if key in self.achievements:
            return

        achievement = ACHIEVEMENTS[key]

        self.achievements[key] = True

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

    def check_achievements(self, guesses_used):

        if self.profile["total_wins"] == 1:
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

        if not self.used_hint:
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

        if self.profile["level"] >= 5:
            self.unlock_achievement(
                "level_five"
            )

    # ========================================================
    # QUESTS
    # ========================================================

    def check_quests(self, guesses_used):

        for quest in self.active_quests:

            name, description, reward = quest

            completed = False

            if name == "First Strike":
                completed = True

            elif name == "Sharp Shooter":
                completed = guesses_used <= 3

            elif name == "Hot Streak":
                completed = self.streak >= 3

            elif name == "Power Player":
                completed = self.power_used

            elif name == "Speed Demon":
                completed = self.time_left >= 10

            elif name == "High Roller":
                completed = self.current_score >= 300

            elif name == "Hintless Hero":
                completed = not self.used_hint

            if completed and name not in self.completed_quests:

                self.completed_quests.append(name)

                self.statistics[
                    "completed_quests"
                ] += 1

                self.add_xp(reward)

                messagebox.showinfo(
                    "🎯 Quest Complete!",
                    f"{name}\n\n"
                    f"{description}\n\n"
                    f"+{reward} XP"
                )

        self.update_quest_display()

    # ========================================================
    # LEADERBOARD
    # ========================================================

    def record_leaderboard(self):

        entry = {
            "name": self.player_name,
            "score": self.current_score,
            "difficulty": self.current_difficulty
        }

        self.leaderboard.append(entry)

        self.leaderboard.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        self.leaderboard = self.leaderboard[:10]

        save_json(
            SAVE_FILE,
            self.leaderboard
        )

    def show_leaderboard(self):

        window = tk.Toplevel(self.root)
        window.title("🏆 Leaderboard")
        window.geometry("600x500")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="🏆 TOP PLAYERS",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(pady=20)

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
    # ACHIEVEMENT WINDOW
    # ========================================================

    def show_achievements(self):

        window = tk.Toplevel(self.root)
        window.title("🎖 Achievement Hall")
        window.geometry("700x620")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="🎖 ACHIEVEMENT HALL",
            font=("Segoe UI", 20, "bold"),
            bg=BG,
            fg=ORANGE
        ).pack(pady=15)

        unlocked = len(self.achievements)

        tk.Label(
            window,
            text=f"{unlocked}/{len(ACHIEVEMENTS)} Unlocked",
            font=("Segoe UI", 11, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=(0, 15))

        for key, achievement in ACHIEVEMENTS.items():

            is_unlocked = key in self.achievements

            if is_unlocked:

                status = "✅ UNLOCKED"
                color = GREEN

            else:

                status = "🔒 LOCKED"
                color = GRAY

            frame = tk.Frame(
                window,
                bg=PANEL
            )
            frame.pack(
                fill="x",
                padx=25,
                pady=4
            )

            tk.Label(
                frame,
                text=achievement["icon"],
                font=("Segoe UI Emoji", 18),
                bg=PANEL,
                fg=WHITE
            ).pack(
                side="left",
                padx=10
            )

            tk.Label(
                frame,
                text=achievement["name"],
                font=("Segoe UI", 11, "bold"),
                bg=PANEL,
                fg=WHITE
            ).pack(
                side="left"
            )

            tk.Label(
                frame,
                text=achievement["description"],
                font=("Segoe UI", 9),
                bg=PANEL,
                fg=GRAY
            ).pack(
                side="left",
                padx=15
            )

            tk.Label(
                frame,
                text=status,
                font=("Segoe UI", 9, "bold"),
                bg=PANEL,
                fg=color
            ).pack(
                side="right",
                padx=10
            )

    # ========================================================
    # PROFILE WINDOW
    # ========================================================

    def show_profile(self):

        window = tk.Toplevel(self.root)
        window.title("👤 Player Profile")
        window.geometry("720x650")
        window.configure(bg=BG)

        tk.Label(
            window,
            text="👤 PLAYER PROFILE",
            font=("Segoe UI", 24, "bold"),
            bg=BG,
            fg=CYAN
        ).pack(pady=(20, 3))

        tk.Label(
            window,
            text=self.player_name,
            font=("Segoe UI", 16, "bold"),
            bg=BG,
            fg=WHITE
        ).pack()

        tk.Label(
            window,
            text=f"⭐ Level {self.profile['level']}",
            font=("Segoe UI", 12, "bold"),
            bg=BG,
            fg=YELLOW
        ).pack(pady=5)

        stats_frame = tk.Frame(
            window,
            bg=BG
        )
        stats_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=20
        )

        total_games = self.profile["total_games"]
        wins = self.profile["total_wins"]

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

        total_guesses = self.statistics[
            "total_guesses"
        ]

        if total_games > 0:
            average_guesses = (
                total_guesses / total_games
            )
        else:
            average_guesses = 0

        unlocked = len(
            self.achievements
        )

        rows = [
            ("🎮 Total Games", total_games),
            ("🏆 Total Wins", wins),
            ("💥 Total Losses", losses),
            ("📈 Win Rate", f"{win_rate:.1f}%"),
            ("💯 Highest Score", self.statistics["highest_score"]),
            ("🔥 Best Streak", self.profile["best_streak"]),
            ("🎯 Average Guesses", f"{average_guesses:.1f}"),
            ("⭐ Total XP Earned", self.statistics["total_xp_earned"]),
            ("👑 Highest Level", self.statistics["highest_level"]),
            ("🎖 Achievements", f"{unlocked}/{len(ACHIEVEMENTS)}"),
            ("🎯 Quests Completed", self.statistics["completed_quests"])
        ]

        for title, value in rows:

            row = tk.Frame(
                stats_frame,
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

        tk.Label(
            window,
            text="📊 DIFFICULTY STATISTICS",
            font=("Segoe UI", 13, "bold"),
            bg=BG,
            fg=PURPLE
        ).pack(pady=(5, 10))

        difficulty_text = ""

        for difficulty, data in self.statistics[
            "difficulty"
        ].items():

            difficulty_text += (
                f"{difficulty}: "
                f"{data['wins']}/{data['games']} wins   "
                f"| Score: {data['score']}\n"
            )

        tk.Label(
            window,
            text=difficulty_text,
            font=("Segoe UI", 10),
            bg=BG,
            fg=WHITE,
            justify="center"
        ).pack(pady=5)

    # ========================================================
    # DISPLAY
    # ========================================================

    def update_game_display(self):

        self.score_label.config(
            text=f"⭐ Score: {self.current_score}"
        )

        self.streak_label.config(
            text=f"🔥 Streak: {self.streak}   "
                 f"Combo: x{self.combo}"
        )

        self.attempts_label.config(
            text=f"Attempts Remaining: {self.attempts_left}"
        )

        self.update_profile_display()

    def update_profile_display(self):

        level = self.profile["level"]
        xp = self.profile["xp"]

        self.player_display.config(
            text=self.player_name
        )

        self.level_display.config(
            text=f"⭐ Level {level}"
        )

        self.xp_label.config(
            text=f"XP: {xp}/{level * 250}"
        )

        self.xp_bar.delete("all")

        progress = min(
            1,
            xp / (level * 250)
        )

        self.xp_bar.create_rectangle(
            0,
            0,
            210 * progress,
            16,
            fill=PURPLE,
            outline=""
        )

        total_games = self.profile["total_games"]
        wins = self.profile["total_wins"]

        if total_games > 0:
            win_rate = (
                wins / total_games
            ) * 100
        else:
            win_rate = 0

        self.quick_stats.config(
            text=(
                f"🎮 Games: {total_games}\n"
                f"🏆 Wins: {wins}\n"
                f"📈 Win Rate: {win_rate:.1f}%\n"
                f"🔥 Best Streak: "
                f"{self.profile['best_streak']}\n"
                f"💯 High Score: "
                f"{self.statistics['highest_score']}\n"
                f"🎖 Badges: "
                f"{len(self.achievements)}/"
                f"{len(ACHIEVEMENTS)}"
            )
        )

        self.update_quest_display()

    def update_quest_display(self):

        text = ""

        for name, description, reward in self.active_quests:

            if name in self.completed_quests:
                mark = "✅"
            else:
                mark = "⬜"

            text += (
                f"{mark} {name}\n"
                f"   {description}\n"
                f"   +{reward} XP\n\n"
            )

        self.quest_label.config(
            text=text
        )

    # ========================================================
    # SAVE
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
# START GAME
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = NumberGuessingGame(root)

    root.mainloop()
    