import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import time

# ============================================================
# NUMBER GUESSING GAME V27
# QUEST & XP EDITION
# ============================================================

SAVE_FILE = "leaderboard_v27.json"
PROFILE_FILE = "player_profile_v27.json"

# ---------------- COLORS ----------------

BG = "#0B1020"
PANEL = "#151C35"
PANEL2 = "#1D2747"

PURPLE = "#9B59FF"
BLUE = "#3498DB"
CYAN = "#00E5FF"
GREEN = "#2ECC71"
YELLOW = "#F1C40F"
ORANGE = "#FF9F43"
RED = "#FF4757"
PINK = "#FF4FA3"
WHITE = "#FFFFFF"
GRAY = "#AAB4D4"

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

QUEST_POOL = [
    {
        "name": "First Strike",
        "description": "Win 1 game",
        "target": 1,
        "reward": 50,
        "type": "wins"
    },
    {
        "name": "Sharp Shooter",
        "description": "Win within 3 guesses",
        "target": 1,
        "reward": 75,
        "type": "quick_win"
    },
    {
        "name": "Hot Streak",
        "description": "Reach a 3-win streak",
        "target": 3,
        "reward": 100,
        "type": "streak"
    },
    {
        "name": "Power Player",
        "description": "Use a power-up and win",
        "target": 1,
        "reward": 75,
        "type": "power_win"
    },
    {
        "name": "Speed Demon",
        "description": "Win with 10+ seconds remaining",
        "target": 1,
        "reward": 100,
        "type": "speed_win"
    },
    {
        "name": "High Roller",
        "description": "Score 300+ points in one game",
        "target": 1,
        "reward": 100,
        "type": "high_score"
    },
    {
        "name": "Hintless Hero",
        "description": "Win without using a hint",
        "target": 1,
        "reward": 100,
        "type": "no_hint"
    }
]


# ============================================================
# MAIN CLASS
# ============================================================

class NumberGuessingGame:

    def __init__(self, root):
        self.root = root

        self.root.title("🎯 Number Guessing Game V27 - Quest & XP Edition")
        self.root.geometry("1100x720")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ---------------- GAME VARIABLES ----------------

        self.difficulty = "Medium"
        self.mode = "Single Player"

        self.secret_number = 0
        self.max_number = 100
        self.attempts_left = 10
        self.total_attempts = 10

        self.timer_seconds = 60
        self.timer_running = False
        self.timer_job = None

        self.hints_left = 3

        self.score = 0
        self.streak = 0
        self.best_streak = 0

        self.current_player = 1

        # Power-ups
        self.extra_life_available = True
        self.time_freeze_available = True
        self.double_score_available = True
        self.range_reveal_available = True
        self.double_score_active = False

        self.freeze_active = False

        self.used_hint = False
        self.used_powerup = False

        # Tournament
        self.tournament_round = 0
        self.tournament_total = 3
        self.tournament_scores = [0, 0]

        # ---------------- PROFILE ----------------

        self.xp = 0
        self.level = 1
        self.total_wins = 0
        self.total_games = 0

        self.load_profile()

        # ---------------- LEADERBOARD ----------------

        self.leaderboard = self.load_leaderboard()

        # ---------------- QUESTS ----------------

        self.quests = []
        self.generate_quests()

        # ---------------- UI ----------------

        self.create_header()
        self.create_left_panel()
        self.create_game_panel()
        self.create_right_panel()

        self.update_profile_display()
        self.update_quest_display()

        self.new_game()

    # ========================================================
    # PROFILE
    # ========================================================

    def load_profile(self):

        if os.path.exists(PROFILE_FILE):

            try:
                with open(PROFILE_FILE, "r") as file:
                    data = json.load(file)

                self.xp = data.get("xp", 0)
                self.level = data.get("level", 1)
                self.total_wins = data.get("total_wins", 0)
                self.total_games = data.get("total_games", 0)

            except Exception:
                pass

    def save_profile(self):

        data = {
            "xp": self.xp,
            "level": self.level,
            "total_wins": self.total_wins,
            "total_games": self.total_games
        }

        try:
            with open(PROFILE_FILE, "w") as file:
                json.dump(data, file, indent=4)
        except Exception:
            pass

    def xp_needed(self):

        return self.level * 250

    def add_xp(self, amount):

        self.xp += amount

        level_up = False

        while self.xp >= self.xp_needed():

            self.xp -= self.xp_needed()
            self.level += 1
            level_up = True

        self.save_profile()
        self.update_profile_display()

        if level_up:

            messagebox.showinfo(
                "🎉 LEVEL UP!",
                f"Congratulations!\n\nYou reached LEVEL {self.level}!"
            )

    # ========================================================
    # LEADERBOARD
    # ========================================================

    def load_leaderboard(self):

        if os.path.exists(SAVE_FILE):

            try:
                with open(SAVE_FILE, "r") as file:
                    return json.load(file)
            except Exception:
                pass

        return {}

    def save_leaderboard(self):

        try:
            with open(SAVE_FILE, "w") as file:
                json.dump(self.leaderboard, file, indent=4)
        except Exception:
            pass

    def record_player(self, name="Player"):

        if name not in self.leaderboard:

            self.leaderboard[name] = {
                "wins": 0,
                "games": 0,
                "best_score": 0,
                "best_streak": 0
            }

        self.leaderboard[name]["games"] += 1

        if self.score > self.leaderboard[name]["best_score"]:
            self.leaderboard[name]["best_score"] = self.score

        if self.streak > self.leaderboard[name]["best_streak"]:
            self.leaderboard[name]["best_streak"] = self.streak

        self.save_leaderboard()

    # ========================================================
    # QUEST SYSTEM
    # ========================================================

    def generate_quests(self):

        selected = random.sample(
            QUEST_POOL,
            min(3, len(QUEST_POOL))
        )

        self.quests = []

        for quest in selected:

            self.quests.append({
                "name": quest["name"],
                "description": quest["description"],
                "target": quest["target"],
                "reward": quest["reward"],
                "type": quest["type"],
                "progress": 0,
                "completed": False
            })

    def update_quest(self, event_type, value=1):

        completed_messages = []

        for quest in self.quests:

            if quest["completed"]:
                continue

            should_update = False

            if quest["type"] == event_type:
                should_update = True

            if should_update:

                quest["progress"] += value

                if quest["progress"] >= quest["target"]:

                    quest["progress"] = quest["target"]
                    quest["completed"] = True

                    self.add_xp(quest["reward"])

                    completed_messages.append(
                        f"🏆 {quest['name']}  +{quest['reward']} XP"
                    )

        self.update_quest_display()

        if completed_messages:

            messagebox.showinfo(
                "🎯 QUEST COMPLETED!",
                "\n".join(completed_messages)
            )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=BG,
            height=80
        )

        header.pack(fill="x", padx=20, pady=(15, 5))

        title = tk.Label(
            header,
            text="🎯 NUMBER GUESSING ARCADE",
            font=("Arial", 26, "bold"),
            fg=CYAN,
            bg=BG
        )

        title.pack(side="left")

        self.profile_label = tk.Label(
            header,
            text="⭐ Level 1 | XP 0/250",
            font=("Arial", 13, "bold"),
            fg=YELLOW,
            bg=BG
        )

        self.profile_label.pack(side="right", pady=10)

    # ========================================================
    # LEFT PANEL
    # ========================================================

    def create_left_panel(self):

        self.left_panel = tk.Frame(
            self.root,
            bg=PANEL,
            width=220,
            height=590
        )

        self.left_panel.pack(
            side="left",
            padx=(20, 10),
            pady=10,
            fill="y"
        )

        self.left_panel.pack_propagate(False)

        tk.Label(
            self.left_panel,
            text="🎮 GAME SETTINGS",
            font=("Arial", 14, "bold"),
            fg=PINK,
            bg=PANEL
        ).pack(pady=15)

        tk.Label(
            self.left_panel,
            text="Difficulty",
            font=("Arial", 11, "bold"),
            fg=WHITE,
            bg=PANEL
        ).pack()

        self.difficulty_var = tk.StringVar(value="Medium")

        for difficulty in ["Easy", "Medium", "Hard"]:

            tk.Radiobutton(
                self.left_panel,
                text=difficulty,
                variable=self.difficulty_var,
                value=difficulty,
                command=self.change_difficulty,
                bg=PANEL,
                fg=WHITE,
                selectcolor=PANEL2,
                activebackground=PANEL,
                activeforeground=CYAN,
                font=("Arial", 10)
            ).pack(anchor="w", padx=35, pady=3)

        tk.Label(
            self.left_panel,
            text="Mode",
            font=("Arial", 11, "bold"),
            fg=WHITE,
            bg=PANEL
        ).pack(pady=(20, 5))

        self.mode_var = tk.StringVar(value="Single Player")

        for mode in ["Single Player", "Two Player", "Tournament"]:

            tk.Radiobutton(
                self.left_panel,
                text=mode,
                variable=self.mode_var,
                value=mode,
                command=self.change_mode,
                bg=PANEL,
                fg=WHITE,
                selectcolor=PANEL2,
                activebackground=PANEL,
                activeforeground=CYAN,
                font=("Arial", 10)
            ).pack(anchor="w", padx=20, pady=3)

        tk.Button(
            self.left_panel,
            text="🔄 NEW GAME",
            command=self.new_game,
            bg=PURPLE,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=8
        ).pack(pady=20)

        tk.Button(
            self.left_panel,
            text="🏆 LEADERBOARD",
            command=self.show_leaderboard,
            bg=ORANGE,
            fg=WHITE,
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=8
        ).pack()

    # ========================================================
    # GAME PANEL
    # ========================================================

    def create_game_panel(self):

        self.game_panel = tk.Frame(
            self.root,
            bg=PANEL2,
            width=540,
            height=590
        )

        self.game_panel.pack(
            side="left",
            padx=10,
            pady=10,
            fill="both",
            expand=True
        )

        self.game_panel.pack_propagate(False)

        self.status_label = tk.Label(
            self.game_panel,
            text="Guess the secret number!",
            font=("Arial", 17, "bold"),
            fg=WHITE,
            bg=PANEL2
        )

        self.status_label.pack(pady=(20, 15))

        self.range_label = tk.Label(
            self.game_panel,
            text="Number between 1 and 100",
            font=("Arial", 13),
            fg=CYAN,
            bg=PANEL2
        )

        self.range_label.pack()

        self.timer_label = tk.Label(
            self.game_panel,
            text="⏱ 60",
            font=("Arial", 18, "bold"),
            fg=YELLOW,
            bg=PANEL2
        )

        self.timer_label.pack(pady=12)

        self.attempt_label = tk.Label(
            self.game_panel,
            text="Attempts: 10",
            font=("Arial", 12, "bold"),
            fg=GREEN,
            bg=PANEL2
        )

        self.attempt_label.pack()

        self.guess_entry = tk.Entry(
            self.game_panel,
            font=("Arial", 20, "bold"),
            justify="center",
            bg=BG,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )

        self.guess_entry.pack(
            pady=15,
            ipadx=15,
            ipady=8
        )

        self.guess_entry.bind(
            "<Return>",
            lambda event: self.check_guess()
        )

        tk.Button(
            self.game_panel,
            text="🎯 GUESS",
            command=self.check_guess,
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 13, "bold"),
            relief="flat",
            padx=35,
            pady=10
        ).pack()

        self.feedback_label = tk.Label(
            self.game_panel,
            text="",
            font=("Arial", 13, "bold"),
            fg=WHITE,
            bg=PANEL2,
            wraplength=450
        )

        self.feedback_label.pack(pady=15)

        # ---------------- POWER UPS ----------------

        power_frame = tk.Frame(
            self.game_panel,
            bg=PANEL2
        )

        power_frame.pack(pady=5)

        tk.Label(
            power_frame,
            text="⚡ POWER-UPS",
            font=("Arial", 12, "bold"),
            fg=ORANGE,
            bg=PANEL2
        ).grid(row=0, column=0, columnspan=2, pady=5)

        self.extra_button = tk.Button(
            power_frame,
            text="❤️ +2 Lives",
            command=self.use_extra_life,
            bg=RED,
            fg=WHITE,
            relief="flat"
        )

        self.extra_button.grid(row=1, column=0, padx=5, pady=3)

        self.freeze_button = tk.Button(
            power_frame,
            text="❄️ Freeze",
            command=self.use_time_freeze,
            bg=CYAN,
            fg=BG,
            relief="flat"
        )

        self.freeze_button.grid(row=1, column=1, padx=5, pady=3)

        self.double_button = tk.Button(
            power_frame,
            text="⭐ 2X Score",
            command=self.use_double_score,
            bg=YELLOW,
            fg=BG,
            relief="flat"
        )

        self.double_button.grid(row=2, column=0, padx=5, pady=3)

        self.range_button = tk.Button(
            power_frame,
            text="🔍 Reveal Range",
            command=self.use_range_reveal,
            bg=GREEN,
            fg=WHITE,
            relief="flat"
        )

        self.range_button.grid(row=2, column=1, padx=5, pady=3)

        # ---------------- STATS ----------------

        self.stats_label = tk.Label(
            self.game_panel,
            text="⭐ Score: 0    🔥 Streak: 0",
            font=("Arial", 12, "bold"),
            fg=PINK,
            bg=PANEL2
        )

        self.stats_label.pack(pady=15)

    # ========================================================
    # RIGHT PANEL
    # ========================================================

    def create_right_panel(self):

        self.right_panel = tk.Frame(
            self.root,
            bg=PANEL,
            width=250,
            height=590
        )

        self.right_panel.pack(
            side="right",
            padx=(10, 20),
            pady=10,
            fill="y"
        )

        self.right_panel.pack_propagate(False)

        tk.Label(
            self.right_panel,
            text="🎯 ACTIVE QUESTS",
            font=("Arial", 14, "bold"),
            fg=YELLOW,
            bg=PANEL
        ).pack(pady=15)

        self.quest_frame = tk.Frame(
            self.right_panel,
            bg=PANEL
        )

        self.quest_frame.pack(fill="both", padx=10)

        tk.Label(
            self.right_panel,
            text="━━━━━━━━━━━━━━",
            fg=PURPLE,
            bg=PANEL
        ).pack(pady=10)

        tk.Label(
            self.right_panel,
            text="📊 PROFILE",
            font=("Arial", 13, "bold"),
            fg=CYAN,
            bg=PANEL
        ).pack()

        self.profile_stats = tk.Label(
            self.right_panel,
            text="",
            font=("Arial", 10),
            fg=WHITE,
            bg=PANEL,
            justify="left"
        )

        self.profile_stats.pack(pady=10)

    # ========================================================
    # PROFILE DISPLAY
    # ========================================================

    def update_profile_display(self):

        needed = self.xp_needed()

        self.profile_label.config(
            text=f"⭐ Level {self.level} | XP {self.xp}/{needed}"
        )

        self.profile_stats.config(
            text=(
                f"⭐ Level: {self.level}\n"
                f"✨ XP: {self.xp}/{needed}\n"
                f"🏆 Total Wins: {self.total_wins}\n"
                f"🎮 Games: {self.total_games}\n"
                f"🔥 Best Streak: {self.best_streak}"
            )
        )

    # ========================================================
    # QUEST DISPLAY
    # ========================================================

    def update_quest_display(self):

        for widget in self.quest_frame.winfo_children():
            widget.destroy()

        for quest in self.quests:

            if quest["completed"]:

                color = GREEN
                status = "✅ COMPLETED"

            else:

                color = WHITE
                status = (
                    f"{quest['progress']}/{quest['target']}"
                )

            card = tk.Frame(
                self.quest_frame,
                bg=PANEL2,
                padx=8,
                pady=8
            )

            card.pack(
                fill="x",
                pady=6
            )

            tk.Label(
                card,
                text=f"🎯 {quest['name']}",
                font=("Arial", 10, "bold"),
                fg=color,
                bg=PANEL2
            ).pack(anchor="w")

            tk.Label(
                card,
                text=quest["description"],
                font=("Arial", 9),
                fg=GRAY,
                bg=PANEL2,
                wraplength=190,
                justify="left"
            ).pack(anchor="w", pady=3)

            tk.Label(
                card,
                text=f"{status}   +{quest['reward']} XP",
                font=("Arial", 9, "bold"),
                fg=YELLOW,
                bg=PANEL2
            ).pack(anchor="w")

    # ========================================================
    # DIFFICULTY
    # ========================================================

    def change_difficulty(self):

        self.difficulty = self.difficulty_var.get()

        self.new_game()

    # ========================================================
    # MODE
    # ========================================================

    def change_mode(self):

        self.mode = self.mode_var.get()

        self.new_game()

    # ========================================================
    # NEW GAME
    # ========================================================

    def new_game(self):

        self.stop_timer()

        settings = DIFFICULTIES[self.difficulty]

        self.max_number = settings["max"]

        self.total_attempts = settings["attempts"]
        self.attempts_left = settings["attempts"]

        self.timer_seconds = settings["time"]

        self.secret_number = random.randint(
            1,
            self.max_number
        )

        self.hints_left = 3

        self.score = 0

        self.used_hint = False
        self.used_powerup = False

        self.double_score_active = False
        self.freeze_active = False

        self.extra_life_available = True
        self.time_freeze_available = True
        self.double_score_available = True
        self.range_reveal_available = True

        self.extra_button.config(state="normal")
        self.freeze_button.config(state="normal")
        self.double_button.config(state="normal")
        self.range_button.config(state="normal")

        self.current_player = 1

        self.range_label.config(
            text=f"Number between 1 and {self.max_number}"
        )

        self.feedback_label.config(
            text="🎯 Make your guess!"
        )

        self.update_attempt_display()
        self.update_stats()

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

        self.start_timer()

    # ========================================================
    # TIMER
    # ========================================================

    def start_timer(self):

        self.stop_timer()

        self.timer_running = True

        self.timer_tick()

    def stop_timer(self):

        self.timer_running = False

        if self.timer_job:

            try:
                self.root.after_cancel(self.timer_job)
            except Exception:
                pass

            self.timer_job = None

    def timer_tick(self):

        if not self.timer_running:
            return

        self.timer_label.config(
            text=f"⏱ {self.timer_seconds}"
        )

        if self.timer_seconds <= 10:

            self.timer_label.config(
                fg=RED
            )

        else:

            self.timer_label.config(
                fg=YELLOW
            )

        if self.timer_seconds <= 0:

            self.timer_running = False

            self.feedback_label.config(
                text=f"⏰ Time's up! Number was {self.secret_number}",
                fg=RED
            )

            self.game_lost()

            return

        self.timer_seconds -= 1

        self.timer_job = self.root.after(
            1000,
            self.timer_tick
        )

    # ========================================================
    # GUESS
    # ========================================================

    def check_guess(self):

        value = self.guess_entry.get().strip()

        if not value.isdigit():

            self.feedback_label.config(
                text="⚠️ Enter a valid number!",
                fg=RED
            )

            return

        guess = int(value)

        if guess < 1 or guess > self.max_number:

            self.feedback_label.config(
                text=f"⚠️ Enter a number from 1 to {self.max_number}",
                fg=RED
            )

            return

        self.attempts_left -= 1

        self.update_attempt_display()

        if guess == self.secret_number:

            self.game_won()

            return

        if guess < self.secret_number:

            self.feedback_label.config(
                text="📈 Too LOW! Try a higher number.",
                fg=ORANGE
            )

        else:

            self.feedback_label.config(
                text="📉 Too HIGH! Try a lower number.",
                fg=PINK
            )

        if self.attempts_left <= 0:

            self.game_lost()

    # ========================================================
    # GAME WON
    # ========================================================

    def game_won(self):

        self.stop_timer()

        self.total_games += 1
        self.total_wins += 1

        self.streak += 1

        if self.streak > self.best_streak:
            self.best_streak = self.streak

        settings = DIFFICULTIES[self.difficulty]

        base_score = settings["score"]

        # Attempt bonus
        attempt_bonus = self.attempts_left * 10

        # Time bonus
        time_bonus = self.timer_seconds * 2

        reward = (
            base_score +
            attempt_bonus +
            time_bonus
        )

        # Streak bonus
        reward += self.streak * 20

        # Double score
        if self.double_score_active:
            reward *= 2

        self.score = reward

        self.feedback_label.config(
            text=(
                f"🎉 CORRECT!\n"
                f"The number was {self.secret_number}\n"
                f"⭐ Score: {self.score}"
            ),
            fg=GREEN
        )

        self.add_xp(50)

        # Quest updates
        self.update_quest("wins")

        if self.attempts_left >= self.total_attempts - 3:

            self.update_quest("quick_win")

        if self.streak >= 3:

            self.update_quest(
                "streak",
                self.streak
            )

        if self.used_powerup:

            self.update_quest("power_win")

        if self.timer_seconds >= 10:

            self.update_quest("speed_win")

        if self.score >= 300:

            self.update_quest("high_score")

        if not self.used_hint:

            self.update_quest("no_hint")

        self.record_player()

        self.save_profile()

        self.update_stats()
        self.update_profile_display()

        self.root.after(
            2200,
            self.new_game
        )

    # ========================================================
    # GAME LOST
    # ========================================================

    def game_lost(self):

        self.stop_timer()

        self.total_games += 1

        self.streak = 0

        self.feedback_label.config(
            text=(
                f"💥 GAME OVER!\n"
                f"The number was {self.secret_number}"
            ),
            fg=RED
        )

        self.save_profile()

        self.update_stats()
        self.update_profile_display()

        self.root.after(
            2200,
            self.new_game
        )

    # ========================================================
    # ATTEMPT DISPLAY
    # ========================================================

    def update_attempt_display(self):

        self.attempt_label.config(
            text=f"Attempts: {self.attempts_left}"
        )

    # ========================================================
    # STATS
    # ========================================================

    def update_stats(self):

        self.stats_label.config(
            text=(
                f"⭐ Score: {self.score}    "
                f"🔥 Streak: {self.streak}"
            )
        )

    # ========================================================
    # POWER-UP: EXTRA LIFE
    # ========================================================

    def use_extra_life(self):

        if not self.extra_life_available:
            return

        self.attempts_left += 2

        self.extra_life_available = False
        self.used_powerup = True

        self.extra_button.config(
            state="disabled"
        )

        self.feedback_label.config(
            text="❤️ +2 LIVES ACTIVATED!",
            fg=RED
        )

        self.update_attempt_display()

    # ========================================================
    # POWER-UP: TIME FREEZE
    # ========================================================

    def use_time_freeze(self):

        if not self.time_freeze_available:
            return

        self.time_freeze_available = False
        self.used_powerup = True
        self.freeze_active = True

        self.freeze_button.config(
            state="disabled"
        )

        self.timer_running = False

        self.feedback_label.config(
            text="❄️ TIME FROZEN FOR 10 SECONDS!",
            fg=CYAN
        )

        self.root.after(
            10000,
            self.resume_after_freeze
        )

    def resume_after_freeze(self):

        if self.timer_seconds > 0:

            self.freeze_active = False
            self.timer_running = True

            self.timer_tick()

    # ========================================================
    # POWER-UP: DOUBLE SCORE
    # ========================================================

    def use_double_score(self):

        if not self.double_score_available:
            return

        self.double_score_available = False
        self.double_score_active = True
        self.used_powerup = True

        self.double_button.config(
            state="disabled"
        )

        self.feedback_label.config(
            text="⭐ 2X SCORE ACTIVATED!",
            fg=YELLOW
        )

    # ========================================================
    # POWER-UP: RANGE REVEAL
    # ========================================================

    def use_range_reveal(self):

        if not self.range_reveal_available:
            return

        self.range_reveal_available = False
        self.used_powerup = True

        self.range_button.config(
            state="disabled"
        )

        low = max(
            1,
            self.secret_number - 10
        )

        high = min(
            self.max_number,
            self.secret_number + 10
        )

        self.range_label.config(
            text=f"🔍 Secret is between {low} and {high}",
            fg=GREEN
        )

    # ========================================================
    # LEADERBOARD
    # ========================================================

    def show_leaderboard(self):

        window = tk.Toplevel(self.root)

        window.title("🏆 Leaderboard")
        window.geometry("550x450")

        window.configure(
            bg=BG
        )

        tk.Label(
            window,
            text="🏆 LEADERBOARD",
            font=("Arial", 22, "bold"),
            fg=YELLOW,
            bg=BG
        ).pack(pady=20)

        if not self.leaderboard:

            tk.Label(
                window,
                text="No records yet!",
                font=("Arial", 13),
                fg=WHITE,
                bg=BG
            ).pack()

            return

        sorted_players = sorted(
            self.leaderboard.items(),
            key=lambda item: item[1]["best_score"],
            reverse=True
        )

        for index, (name, data) in enumerate(
            sorted_players[:10],
            start=1
        ):

            text = (
                f"{index}. {name}   "
                f"⭐ {data['best_score']}   "
                f"🏆 {data['wins']} wins   "
                f"🔥 {data['best_streak']}"
            )

            tk.Label(
                window,
                text=text,
                font=("Arial", 11, "bold"),
                fg=WHITE,
                bg=BG,
                anchor="w"
            ).pack(
                fill="x",
                padx=30,
                pady=7
            )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    game = NumberGuessingGame(root)

    root.mainloop()