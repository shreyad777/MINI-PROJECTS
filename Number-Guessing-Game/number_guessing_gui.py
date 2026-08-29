import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import winsound


# ============================================================
# NUMBER GUESSING GAME - V18
# CUSTOM GAME MODES
# ============================================================

DATA_FILE = "game_data.json"


# ============================================================
# GLOBAL VARIABLES
# ============================================================

secret_number = 0
minimum = 1
maximum = 100

attempts = 0
max_attempts = 10

score = 0
player_name = ""

games_played = 0
games_won = 0
games_lost = 0
best_score = 0
winning_streak = 0

game_history = []
leaderboard = []

timer_seconds = 0
timer_job = None
game_active = False

dark_mode = False
sound_enabled = True

current_multiplier = 2

fastest_win = None
highest_difficulty = "None"

difficulty_name = "Medium"

# V18
game_mode = "Classic Mode"
time_limit = 30
mode_streak = 0


# ============================================================
# MULTIPLAYER VARIABLES
# ============================================================

multiplayer_mode = False
multiplayer_players = []
multiplayer_scores = {}
multiplayer_round = 1
multiplayer_total_rounds = 5
current_player_index = 0
multiplayer_secret = 0
multiplayer_attempts = 0
multiplayer_game_active = False


# ============================================================
# DIFFICULTY SETTINGS
# ============================================================

DIFFICULTY_SETTINGS = {
    "Easy": {
        "minimum": 1,
        "maximum": 50,
        "attempts": 12,
        "multiplier": 1
    },

    "Medium": {
        "minimum": 1,
        "maximum": 100,
        "attempts": 10,
        "multiplier": 2
    },

    "Hard": {
        "minimum": 1,
        "maximum": 200,
        "attempts": 8,
        "multiplier": 3
    }
}


# ============================================================
# GAME MODE SETTINGS
# ============================================================

GAME_MODES = [
    "Classic Mode",
    "Time Challenge",
    "Sudden Death",
    "Streak Mode"
]


# ============================================================
# DIFFICULTY STATISTICS
# ============================================================

difficulty_statistics = {
    "Easy": {
        "played": 0,
        "won": 0,
        "lost": 0,
        "total_score": 0,
        "total_attempts": 0
    },

    "Medium": {
        "played": 0,
        "won": 0,
        "lost": 0,
        "total_score": 0,
        "total_attempts": 0
    },

    "Hard": {
        "played": 0,
        "won": 0,
        "lost": 0,
        "total_score": 0,
        "total_attempts": 0
    }
}


# ============================================================
# ACHIEVEMENTS
# ============================================================

achievements = {
    "First Victory": False,
    "Winning Streak": False,
    "Speed Demon": False,
    "Perfect Guesser": False,
    "Score Master": False,
    "Leaderboard Champion": False,
    "Time Challenger": False,
    "Sudden Death Survivor": False,
    "Streak Master": False
}


# ============================================================
# COLORS
# ============================================================

LIGHT_BG = "#f4f6f8"
LIGHT_FG = "#1f2937"
LIGHT_FRAME = "#ffffff"
LIGHT_BUTTON = "#2563eb"

DARK_BG = "#111827"
DARK_FG = "#f9fafb"
DARK_FRAME = "#1f2937"
DARK_BUTTON = "#374151"


# ============================================================
# SOUND
# ============================================================

def play_sound(sound_type):

    if not sound_enabled:
        return

    try:

        if sound_type == "correct":
            winsound.Beep(1000, 150)

        elif sound_type == "high":
            winsound.Beep(500, 120)

        elif sound_type == "low":
            winsound.Beep(300, 120)

        elif sound_type == "win":

            winsound.Beep(1000, 150)
            winsound.Beep(1300, 150)
            winsound.Beep(1600, 200)

        elif sound_type == "lose":

            winsound.Beep(500, 200)
            winsound.Beep(300, 300)

        elif sound_type == "achievement":

            winsound.Beep(1000, 100)
            winsound.Beep(1300, 100)
            winsound.Beep(1600, 200)

    except Exception:
        pass


def toggle_sound():

    global sound_enabled

    sound_enabled = not sound_enabled

    save_data()
    update_sound_button()

    if sound_enabled:
        play_sound("correct")


def update_sound_button():

    if sound_enabled:
        sound_button.config(text="🔊 SOUND ON")

    else:
        sound_button.config(text="🔇 SOUND OFF")


# ============================================================
# DATA LOADING
# ============================================================

def load_data():

    if not os.path.exists(DATA_FILE):
        return

    try:

        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        global games_played
        global games_won
        global games_lost
        global best_score
        global winning_streak
        global game_history
        global leaderboard
        global sound_enabled
        global fastest_win
        global highest_difficulty
        global difficulty_statistics
        global achievements

        games_played = data.get(
            "games_played",
            0
        )

        games_won = data.get(
            "games_won",
            0
        )

        games_lost = data.get(
            "games_lost",
            0
        )

        best_score = data.get(
            "best_score",
            0
        )

        winning_streak = data.get(
            "winning_streak",
            0
        )

        game_history = data.get(
            "game_history",
            []
        )

        leaderboard = data.get(
            "leaderboard",
            []
        )

        sound_enabled = data.get(
            "sound_enabled",
            True
        )

        fastest_win = data.get(
            "fastest_win",
            None
        )

        highest_difficulty = data.get(
            "highest_difficulty",
            "None"
        )

        saved_statistics = data.get(
            "difficulty_statistics",
            {}
        )

        for difficulty in difficulty_statistics:

            if difficulty in saved_statistics:

                difficulty_statistics[
                    difficulty
                ].update(
                    saved_statistics[difficulty]
                )

        saved_achievements = data.get(
            "achievements",
            {}
        )

        for achievement in achievements:

            if achievement in saved_achievements:

                achievements[
                    achievement
                ] = saved_achievements[
                    achievement
                ]

    except (json.JSONDecodeError, OSError):

        print("Unable to load saved data.")


# ============================================================
# SAVE DATA
# ============================================================

def save_data():

    data = {

        "games_played": games_played,

        "games_won": games_won,

        "games_lost": games_lost,

        "best_score": best_score,

        "winning_streak": winning_streak,

        "game_history": game_history,

        "leaderboard": leaderboard,

        "sound_enabled": sound_enabled,

        "fastest_win": fastest_win,

        "highest_difficulty": highest_difficulty,

        "difficulty_statistics":
            difficulty_statistics,

        "achievements":
            achievements
    }

    try:

        with open(
            DATA_FILE,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except OSError:

        print("Unable to save game data.")


load_data()


# ============================================================
# DASHBOARD
# ============================================================

def update_dashboard():

    played_value.config(
        text=str(games_played)
    )

    won_value.config(
        text=str(games_won)
    )

    lost_value.config(
        text=str(games_lost)
    )

    best_value.config(
        text=str(best_score)
    )


# ============================================================
# DIFFICULTY
# ============================================================

def set_difficulty():

    global minimum
    global maximum
    global max_attempts
    global current_multiplier
    global difficulty_name

    difficulty_name = difficulty_var.get()

    settings = DIFFICULTY_SETTINGS[
        difficulty_name
    ]

    minimum = settings["minimum"]

    maximum = settings["maximum"]

    max_attempts = settings["attempts"]

    current_multiplier = settings["multiplier"]

    start_new_game()


# ============================================================
# TIMER
# ============================================================

def format_time(seconds):

    minutes = seconds // 60

    remaining_seconds = seconds % 60

    return (
        f"{minutes:02d}:"
        f"{remaining_seconds:02d}"
    )


def update_timer():

    global timer_seconds
    global timer_job

    if not game_active:
        return

    timer_seconds += 1

    timer_value.config(
        text=format_time(timer_seconds)
    )

    # V18 TIME CHALLENGE

    if (
        game_mode == "Time Challenge"
        and timer_seconds >= time_limit
    ):

        time_challenge_failed()

        return

    timer_job = root.after(
        1000,
        update_timer
    )


def start_timer():

    global game_active
    global timer_seconds
    global timer_job

    if timer_job is not None:

        try:

            root.after_cancel(
                timer_job
            )

        except tk.TclError:
            pass

    timer_seconds = 0

    game_active = True

    timer_value.config(
        text="00:00"
    )

    timer_job = root.after(
        1000,
        update_timer
    )


def stop_timer():

    global game_active
    global timer_job

    game_active = False

    if timer_job is not None:

        try:

            root.after_cancel(
                timer_job
            )

        except tk.TclError:
            pass

        timer_job = None


# ============================================================
# PLAYER START
# ============================================================

def start_player_game():

    global player_name
    global multiplayer_mode

    player_name = (
        name_entry.get().strip()
    )

    if not player_name:

        messagebox.showwarning(
            "Name Required",
            "Please enter your name."
        )

        return

    multiplayer_mode = False

    set_difficulty()


# ============================================================
# START NEW GAME
# ============================================================

def start_new_game():

    global secret_number
    global attempts
    global score
    global mode_streak

    if multiplayer_mode:
        return

    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Enter your name first."
        )

        return

    stop_timer()

    secret_number = random.randint(
        minimum,
        maximum
    )

    attempts = 0

    score = 0

    mode_streak = 0

    guess_entry.delete(
        0,
        tk.END
    )

    mode_text = game_mode

    if game_mode == "Time Challenge":

        mode_description = (
            f"You have {time_limit} seconds!"
        )

    elif game_mode == "Sudden Death":

        mode_description = (
            "ONE wrong guess = GAME OVER!"
        )

    elif game_mode == "Streak Mode":

        mode_description = (
            "Build the longest winning streak!"
        )

    else:

        mode_description = (
            "Guess the hidden number!"
        )

    result_label.config(
        text=(
            f"Welcome, {player_name}!\n\n"
            f"🎮 {mode_text}\n"
            f"📊 {difficulty_name}\n\n"
            f"{mode_description}\n\n"
            f"Guess between "
            f"{minimum} and {maximum}."
        )
    )

    attempts_value.config(
        text=f"0 / {max_attempts}"
    )

    score_value.config(
        text="0"
    )

    multiplier_value.config(
        text=f"{current_multiplier}×"
    )

    start_timer()


# ============================================================
# SCORE
# ============================================================

def calculate_score():

    remaining_attempts = (
        max_attempts
        - attempts
        + 1
    )

    base_score = (
        remaining_attempts
        * current_multiplier
    )

    time_bonus = 0

    if timer_seconds <= 10:
        time_bonus = 5

    elif timer_seconds <= 20:
        time_bonus = 3

    elif timer_seconds <= 30:
        time_bonus = 1

    # V18 mode bonuses

    mode_bonus = 0

    if game_mode == "Time Challenge":
        mode_bonus = 10

    elif game_mode == "Sudden Death":
        mode_bonus = 8

    elif game_mode == "Streak Mode":
        mode_bonus = mode_streak * 3

    return (
        base_score
        + time_bonus
        + mode_bonus
    )


# ============================================================
# HISTORY
# ============================================================

def add_history(
    result,
    final_score
):

    record = {

        "player":
            player_name,

        "difficulty":
            difficulty_name,

        "mode":
            game_mode,

        "result":
            result,

        "attempts":
            attempts,

        "score":
            final_score,

        "time":
            format_time(timer_seconds)
    }

    game_history.append(record)

    save_data()


# ============================================================
# LEADERBOARD
# ============================================================

def update_leaderboard():

    global leaderboard

    leaderboard = sorted(
        leaderboard,
        key=lambda entry: (
            -entry["score"],
            entry.get(
                "time_seconds",
                999999
            )
        )
    )

    leaderboard = leaderboard[:10]

    save_data()


def add_to_leaderboard(
    final_score
):

    if final_score <= 0:
        return

    entry = {

        "player":
            player_name,

        "score":
            final_score,

        "time":
            format_time(timer_seconds),

        "time_seconds":
            timer_seconds,

        "difficulty":
            difficulty_name,

        "mode":
            game_mode
    }

    leaderboard.append(entry)

    update_leaderboard()


def show_leaderboard():

    window = tk.Toplevel(root)

    window.title(
        "🏆 Leaderboard"
    )

    window.geometry(
        "900x600"
    )

    background = (
        DARK_BG
        if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG
        if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME
        if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="🏆 LEADERBOARD",
        font=(
            "Segoe UI",
            24,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(pady=20)

    table = tk.Frame(
        window,
        bg=frame_background
    )

    table.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    headers = [
        "Rank",
        "Player",
        "Score",
        "Time",
        "Difficulty",
        "Mode"
    ]

    for column, header in enumerate(
        headers
    ):

        tk.Label(
            table,
            text=header,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=frame_background,
            fg=foreground,
            width=13
        ).grid(
            row=0,
            column=column,
            padx=4,
            pady=12
        )

    if not leaderboard:

        tk.Label(
            table,
            text="No winning games yet.",
            font=(
                "Segoe UI",
                13
            ),
            bg=frame_background,
            fg=foreground
        ).grid(
            row=1,
            column=0,
            columnspan=6,
            pady=50
        )

        return

    for index, entry in enumerate(
        leaderboard,
        start=1
    ):

        if index == 1:
            rank = "🥇 1"

        elif index == 2:
            rank = "🥈 2"

        elif index == 3:
            rank = "🥉 3"

        else:
            rank = str(index)

        values = [

            rank,

            entry["player"],

            str(entry["score"]),

            entry["time"],

            entry["difficulty"],

            entry.get(
                "mode",
                "Classic Mode"
            )
        ]

        for column, value in enumerate(
            values
        ):

            tk.Label(
                table,
                text=value,
                font=(
                    "Segoe UI",
                    10
                ),
                bg=frame_background,
                fg=foreground,
                width=13
            ).grid(
                row=index,
                column=column,
                padx=4,
                pady=8
            )


# ============================================================
# ACHIEVEMENTS
# ============================================================

def unlock_achievement(
    name
):

    if achievements.get(
        name,
        False
    ):

        return False

    achievements[name] = True

    play_sound(
        "achievement"
    )

    save_data()

    return True


def check_achievements(
    final_score
):

    unlocked = []

    if games_won >= 1:

        if unlock_achievement(
            "First Victory"
        ):

            unlocked.append(
                "🏆 First Victory"
            )

    if winning_streak >= 3:

        if unlock_achievement(
            "Winning Streak"
        ):

            unlocked.append(
                "🔥 Winning Streak"
            )

    if timer_seconds < 15:

        if unlock_achievement(
            "Speed Demon"
        ):

            unlocked.append(
                "⚡ Speed Demon"
            )

    if attempts == 1:

        if unlock_achievement(
            "Perfect Guesser"
        ):

            unlocked.append(
                "🎯 Perfect Guesser"
            )

    if final_score >= 10:

        if unlock_achievement(
            "Score Master"
        ):

            unlocked.append(
                "💯 Score Master"
            )

    if game_mode == "Time Challenge":

        if unlock_achievement(
            "Time Challenger"
        ):

            unlocked.append(
                "⏱️ Time Challenger"
            )

    if game_mode == "Sudden Death":

        if unlock_achievement(
            "Sudden Death Survivor"
        ):

            unlocked.append(
                "💀 Sudden Death Survivor"
            )

    if game_mode == "Streak Mode":

        if mode_streak >= 3:

            if unlock_achievement(
                "Streak Master"
            ):

                unlocked.append(
                    "🔥 Streak Master"
                )

    update_leaderboard()

    if leaderboard:

        if (
            leaderboard[0]["player"]
            == player_name
            and
            leaderboard[0]["score"]
            == final_score
        ):

            if unlock_achievement(
                "Leaderboard Champion"
            ):

                unlocked.append(
                    "🥇 Leaderboard Champion"
                )

    return unlocked


# ============================================================
# SINGLE PLAYER GUESS
# ============================================================

def check_guess():

    if multiplayer_mode:

        check_multiplayer_guess()

        return

    check_single_player_guess()


def check_single_player_guess():

    global attempts
    global score
    global best_score
    global games_played
    global games_won
    global games_lost
    global winning_streak
    global fastest_win
    global highest_difficulty
    global mode_streak

    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Enter your name and "
            "start a game first."
        )

        return

    if not game_active:

        messagebox.showwarning(
            "No Active Game",
            "Start a new game first."
        )

        return

    try:

        guess = int(
            guess_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )

        return

    if (
        guess < minimum
        or
        guess > maximum
    ):

        messagebox.showwarning(
            "Out of Range",
            f"Enter a number between "
            f"{minimum} and {maximum}."
        )

        return

    attempts += 1

    attempts_value.config(
        text=(
            f"{attempts} / "
            f"{max_attempts}"
        )
    )

    # --------------------------------------------------------
    # CORRECT
    # --------------------------------------------------------

    if guess == secret_number:

        stop_timer()

        play_sound(
            "win"
        )

        if game_mode == "Streak Mode":

            mode_streak += 1

        score = calculate_score()

        games_played += 1

        games_won += 1

        winning_streak += 1

        difficulty_statistics[
            difficulty_name
        ]["played"] += 1

        difficulty_statistics[
            difficulty_name
        ]["won"] += 1

        difficulty_statistics[
            difficulty_name
        ]["total_score"] += score

        difficulty_statistics[
            difficulty_name
        ]["total_attempts"] += attempts

        if score > best_score:

            best_score = score

        if (
            fastest_win is None
            or
            timer_seconds < fastest_win
        ):

            fastest_win = timer_seconds

        add_history(
            "Won",
            score
        )

        add_to_leaderboard(
            score
        )

        unlocked = check_achievements(
            score
        )

        highest_difficulty = (
            get_highest_difficulty()
        )

        update_dashboard()

        score_value.config(
            text=str(score)
        )

        result_label.config(
            text=(
                f"🎉 CONGRATULATIONS!\n\n"
                f"You found {secret_number}!\n\n"
                f"Mode: {game_mode}\n"
                f"Score: {score}\n"
                f"Attempts: {attempts}\n"
                f"Time: "
                f"{format_time(timer_seconds)}"
            )
        )

        achievement_message = ""

        if unlocked:

            achievement_message = (
                "\n\n🏅 NEW ACHIEVEMENTS!\n"
                +
                "\n".join(unlocked)
            )

        save_data()

        messagebox.showinfo(
            "🎉 You Won!",
            f"Player: {player_name}\n\n"
            f"Mode: {game_mode}\n"
            f"Difficulty: "
            f"{difficulty_name}\n"
            f"Attempts: {attempts}\n"
            f"Score: {score}\n"
            f"Time: "
            f"{format_time(timer_seconds)}\n"
            f"Winning Streak: "
            f"{winning_streak}"
            f"{achievement_message}"
        )

        return

    # --------------------------------------------------------
    # SUDDEN DEATH
    # --------------------------------------------------------

    if game_mode == "Sudden Death":

        sudden_death_loss(
            guess
        )

        return

    # --------------------------------------------------------
    # NORMAL HIGH / LOW
    # --------------------------------------------------------

    if guess < secret_number:

        play_sound(
            "low"
        )

        result_label.config(
            text=(
                "⬇️ TOO LOW!\n"
                "Try again."
            )
        )

    else:

        play_sound(
            "high"
        )

        result_label.config(
            text=(
                "⬆️ TOO HIGH!\n"
                "Try again."
            )
        )

    # --------------------------------------------------------
    # MAX ATTEMPTS
    # --------------------------------------------------------

    if attempts >= max_attempts:

        game_over()


# ============================================================
# GAME OVER
# ============================================================

def game_over():

    global games_played
    global games_lost
    global winning_streak
    global mode_streak

    stop_timer()

    play_sound(
        "lose"
    )

    games_played += 1

    games_lost += 1

    winning_streak = 0

    mode_streak = 0

    difficulty_statistics[
        difficulty_name
    ]["played"] += 1

    difficulty_statistics[
        difficulty_name
    ]["lost"] += 1

    difficulty_statistics[
        difficulty_name
    ]["total_attempts"] += attempts

    add_history(
        "Lost",
        0
    )

    save_data()

    update_dashboard()

    result_label.config(
        text=(
            f"❌ GAME OVER!\n\n"
            f"The number was "
            f"{secret_number}."
        )
    )

    messagebox.showinfo(
        "❌ Game Over",
        f"Better luck next time!\n\n"
        f"The number was "
        f"{secret_number}."
    )


# ============================================================
# TIME CHALLENGE FAILURE
# ============================================================

def time_challenge_failed():

    global games_played
    global games_lost
    global winning_streak
    global mode_streak

    stop_timer()

    play_sound(
        "lose"
    )

    games_played += 1

    games_lost += 1

    winning_streak = 0

    mode_streak = 0

    difficulty_statistics[
        difficulty_name
    ]["played"] += 1

    difficulty_statistics[
        difficulty_name
    ]["lost"] += 1

    difficulty_statistics[
        difficulty_name
    ]["total_attempts"] += attempts

    add_history(
        "Lost - Time Expired",
        0
    )

    save_data()

    update_dashboard()

    result_label.config(
        text=(
            "⏰ TIME'S UP!\n\n"
            f"The number was "
            f"{secret_number}."
        )
    )

    messagebox.showinfo(
        "⏰ Time Challenge",
        "Time limit reached!\n\n"
        f"The number was "
        f"{secret_number}."
    )


# ============================================================
# SUDDEN DEATH
# ============================================================

def sudden_death_loss(
    guess
):

    global games_played
    global games_lost
    global winning_streak
    global mode_streak

    stop_timer()

    play_sound(
        "lose"
    )

    games_played += 1

    games_lost += 1

    winning_streak = 0

    mode_streak = 0

    difficulty_statistics[
        difficulty_name
    ]["played"] += 1

    difficulty_statistics[
        difficulty_name
    ]["lost"] += 1

    difficulty_statistics[
        difficulty_name
    ]["total_attempts"] += attempts

    add_history(
        "Lost - Sudden Death",
        0
    )

    save_data()

    update_dashboard()

    result_label.config(
        text=(
            "💀 SUDDEN DEATH!\n\n"
            "Wrong guess!\n"
            f"The number was "
            f"{secret_number}."
        )
    )

    messagebox.showinfo(
        "💀 Sudden Death",
        "Wrong guess!\n\n"
        "The game ends immediately.\n\n"
        f"The number was "
        f"{secret_number}."
    )


# ============================================================
# GAME MODE SELECTION
# ============================================================

def change_game_mode():

    global game_mode

    game_mode = mode_var.get()

    mode_description = {

        "Classic Mode":
            "Normal number guessing.",

        "Time Challenge":
            f"Guess the number within "
            f"{time_limit} seconds.",

        "Sudden Death":
            "One wrong guess ends the game.",

        "Streak Mode":
            "Build the longest winning streak."
    }

    mode_info_label.config(
        text=mode_description[
            game_mode
        ]
    )


# ============================================================
# PROFILE CALCULATIONS
# ============================================================

def calculate_win_rate():

    if games_played == 0:
        return 0

    return (
        games_won
        / games_played
        * 100
    )


def calculate_average_score():

    if games_won == 0:
        return 0

    total_score = 0

    for game in game_history:

        if game.get(
            "result"
        ) == "Won":

            total_score += game.get(
                "score",
                0
            )

    return (
        total_score
        / games_won
    )


def calculate_average_attempts():

    if games_played == 0:
        return 0

    total_attempts = 0

    for game in game_history:

        total_attempts += game.get(
            "attempts",
            0
        )

    return (
        total_attempts
        / games_played
    )


def get_highest_difficulty():

    highest = 0

    highest_name = "None"

    levels = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }

    for difficulty, stats in (
        difficulty_statistics.items()
    ):

        if stats["won"] > 0:

            if (
                levels[difficulty]
                > highest
            ):

                highest = levels[
                    difficulty
                ]

                highest_name = (
                    difficulty
                )

    return highest_name


# ============================================================
# PROFILE
# ============================================================

def show_profile():

    window = tk.Toplevel(
        root
    )

    window.title(
        "👤 Player Profile"
    )

    window.geometry(
        "900x800"
    )

    background = (
        DARK_BG
        if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG
        if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME
        if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="👤 PLAYER PROFILE",
        font=(
            "Segoe UI",
            26,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(pady=20)

    tk.Label(
        window,
        text=(
            f"Player: "
            f"{player_name if player_name else 'Guest'}"
        ),
        font=(
            "Segoe UI",
            15,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(pady=10)

    stats = tk.Frame(
        window,
        bg=frame_background,
        padx=20,
        pady=20
    )

    stats.pack(
        fill="x",
        padx=30,
        pady=10
    )

    profile_data = [

        (
            "🎮 Games Played",
            str(games_played)
        ),

        (
            "🏆 Games Won",
            str(games_won)
        ),

        (
            "❌ Games Lost",
            str(games_lost)
        ),

        (
            "📈 Win Rate",
            f"{calculate_win_rate():.1f}%"
        ),

        (
            "💯 Best Score",
            str(best_score)
        ),

        (
            "🔥 Winning Streak",
            str(winning_streak)
        ),

        (
            "⚡ Fastest Win",
            (
                format_time(
                    fastest_win
                )
                if fastest_win is not None
                else "N/A"
            )
        ),

        (
            "🎯 Average Score",
            f"{calculate_average_score():.1f}"
        ),

        (
            "📊 Average Attempts",
            f"{calculate_average_attempts():.1f}"
        ),

        (
            "🔴 Highest Difficulty",
            get_highest_difficulty()
        )
    ]

    for index, (
        label,
        value
    ) in enumerate(profile_data):

        row = index // 2

        column = index % 2

        card = tk.Frame(
            stats,
            bg=frame_background,
            padx=20,
            pady=12
        )

        card.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=10,
            pady=6
        )

        tk.Label(
            card,
            text=label,
            font=(
                "Segoe UI",
                10
            ),
            bg=frame_background,
            fg=foreground
        ).pack()

        tk.Label(
            card,
            text=value,
            font=(
                "Segoe UI",
                18,
                "bold"
            ),
            bg=frame_background,
            fg=foreground
        ).pack()

    stats.grid_columnconfigure(
        0,
        weight=1
    )

    stats.grid_columnconfigure(
        1,
        weight=1
    )

    # Difficulty table

    difficulty_frame = tk.LabelFrame(
        window,
        text="  📊 Difficulty Statistics  ",
        font=(
            "Segoe UI",
            12,
            "bold"
        ),
        bg=frame_background,
        fg=foreground,
        padx=20,
        pady=15
    )

    difficulty_frame.pack(
        fill="x",
        padx=30,
        pady=15
    )

    headers = [
        "Difficulty",
        "Played",
        "Won",
        "Lost",
        "Win Rate",
        "Avg Score"
    ]

    for column, header in enumerate(
        headers
    ):

        tk.Label(
            difficulty_frame,
            text=header,
            font=(
                "Segoe UI",
                10,
                "bold"
            ),
            bg=frame_background,
            fg=foreground,
            width=14
        ).grid(
            row=0,
            column=column,
            padx=3,
            pady=8
        )

    for row, difficulty in enumerate(
        [
            "Easy",
            "Medium",
            "Hard"
        ],
        start=1
    ):

        stats_data = (
            difficulty_statistics[
                difficulty
            ]
        )

        played = stats_data[
            "played"
        ]

        won = stats_data[
            "won"
        ]

        lost = stats_data[
            "lost"
        ]

        total_score = stats_data[
            "total_score"
        ]

        if played > 0:

            win_rate = (
                won
                / played
                * 100
            )

        else:

            win_rate = 0

        if won > 0:

            average_score = (
                total_score
                / won
            )

        else:

            average_score = 0

        values = [

            difficulty,

            str(played),

            str(won),

            str(lost),

            f"{win_rate:.1f}%",

            f"{average_score:.1f}"
        ]

        for column, value in enumerate(
            values
        ):

            tk.Label(
                difficulty_frame,
                text=value,
                font=(
                    "Segoe UI",
                    10
                ),
                bg=frame_background,
                fg=foreground,
                width=14
            ).grid(
                row=row,
                column=column,
                padx=3,
                pady=6
            )


# ============================================================
# HISTORY
# ============================================================

def show_history():

    window = tk.Toplevel(
        root
    )

    window.title(
        "📜 Game History"
    )

    window.geometry(
        "850x650"
    )

    background = (
        DARK_BG
        if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG
        if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME
        if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="📜 GAME HISTORY",
        font=(
            "Segoe UI",
            22,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(pady=20)

    if not game_history:

        tk.Label(
            window,
            text="No games played yet.",
            font=(
                "Segoe UI",
                13
            ),
            bg=background,
            fg=foreground
        ).pack(pady=50)

        return

    frame = tk.Frame(
        window,
        bg=frame_background
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    scrollbar = tk.Scrollbar(
        frame
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    text = tk.Text(
        frame,
        font=(
            "Consolas",
            10
        ),
        yscrollcommand=scrollbar.set,
        wrap="none",
        bg=frame_background,
        fg=foreground,
        insertbackground=foreground
    )

    text.pack(
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=text.yview
    )

    for index, game in enumerate(
        reversed(game_history),
        start=1
    ):

        text.insert(
            tk.END,
            f"GAME {index}\n"
        )

        text.insert(
            tk.END,
            f"Player     : "
            f"{game['player']}\n"
        )

        text.insert(
            tk.END,
            f"Difficulty : "
            f"{game['difficulty']}\n"
        )

        text.insert(
            tk.END,
            f"Mode       : "
            f"{game.get('mode', 'Classic Mode')}\n"
        )

        text.insert(
            tk.END,
            f"Result     : "
            f"{game['result']}\n"
        )

        text.insert(
            tk.END,
            f"Attempts   : "
            f"{game['attempts']}\n"
        )

        text.insert(
            tk.END,
            f"Score      : "
            f"{game['score']}\n"
        )

        text.insert(
            tk.END,
            f"Time       : "
            f"{game.get('time', '00:00')}\n"
        )

        text.insert(
            tk.END,
            "-" * 60
            + "\n\n"
        )

    text.config(
        state="disabled"
    )


# ============================================================
# ACHIEVEMENT WINDOW
# ============================================================

def show_achievements():

    window = tk.Toplevel(
        root
    )

    window.title(
        "🏅 Achievements"
    )

    window.geometry(
        "750x750"
    )

    background = (
        DARK_BG
        if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG
        if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME
        if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="🏅 ACHIEVEMENTS",
        font=(
            "Segoe UI",
            25,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(pady=25)

    badge_details = {

        "First Victory":
            "Win your first game.",

        "Winning Streak":
            "Win 3 games consecutively.",

        "Speed Demon":
            "Win in under 15 seconds.",

        "Perfect Guesser":
            "Find the number in one attempt.",

        "Score Master":
            "Achieve a score of 10 or higher.",

        "Leaderboard Champion":
            "Reach #1 on the leaderboard.",

        "Time Challenger":
            "Complete a Time Challenge.",

        "Sudden Death Survivor":
            "Survive Sudden Death mode.",

        "Streak Master":
            "Build a streak of 3 or more."
    }

    icons = {

        "First Victory": "🏆",

        "Winning Streak": "🔥",

        "Speed Demon": "⚡",

        "Perfect Guesser": "🎯",

        "Score Master": "💯",

        "Leaderboard Champion": "🥇",

        "Time Challenger": "⏱️",

        "Sudden Death Survivor": "💀",

        "Streak Master": "🔥"
    }

    container = tk.Frame(
        window,
        bg=frame_background
    )

    container.pack(
        padx=30,
        pady=10,
        fill="both",
        expand=True
    )

    for name in achievements:

        unlocked = achievements[
            name
        ]

        if unlocked:

            title = (
                f"{icons[name]} "
                f"{name}"
            )

            status = (
                "✅ UNLOCKED"
            )

        else:

            title = (
                f"🔒 {name}"
            )

            status = (
                "🔒 LOCKED"
            )

        frame = tk.Frame(
            container,
            bg=frame_background,
            padx=15,
            pady=8
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            frame,
            text=title,
            font=(
                "Segoe UI",
                12,
                "bold"
            ),
            bg=frame_background,
            fg=foreground,
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Label(
            frame,
            text=badge_details[name],
            font=(
                "Segoe UI",
                10
            ),
            bg=frame_background,
            fg=foreground,
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Label(
            frame,
            text=status,
            font=(
                "Segoe UI",
                9,
                "bold"
            ),
            bg=frame_background,
            fg=foreground,
            anchor="w"
        ).pack(
            fill="x"
        )


# ============================================================
# MULTIPLAYER SETUP
# ============================================================

def show_multiplayer_setup():

    setup = tk.Toplevel(
        root
    )

    setup.title(
        "👥 Multiplayer Mode"
    )

    setup.geometry(
        "650x650"
    )

    background = (
        DARK_BG
        if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG
        if dark_mode
        else LIGHT_FG
    )

    setup.config(
        bg=background
    )

    tk.Label(
        setup,
        text="👥 MULTIPLAYER MODE",
        font=(
            "Segoe UI",
            25,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(pady=25)

    tk.Label(
        setup,
        text="Enter 2–4 player names",
        font=(
            "Segoe UI",
            12
        ),
        bg=background,
        fg=foreground
    ).pack()

    entries = []

    for i in range(4):

        frame = tk.Frame(
            setup,
            bg=background
        )

        frame.pack(
            pady=7
        )

        tk.Label(
            frame,
            text=f"Player {i + 1}:",
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=background,
            fg=foreground,
            width=12
        ).pack(
            side="left"
        )

        entry = tk.Entry(
            frame,
            font=(
                "Segoe UI",
                11
            ),
            width=25
        )

        entry.pack(
            side="left"
        )

        entries.append(
            entry
        )

    tk.Label(
        setup,
        text="Number of Rounds:",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(
        pady=(20, 5)
    )

    rounds_var = tk.IntVar(
        value=5
    )

    rounds_spinbox = tk.Spinbox(
        setup,
        from_=1,
        to=20,
        textvariable=rounds_var,
        font=(
            "Segoe UI",
            11
        ),
        width=10
    )

    rounds_spinbox.pack()

    tk.Label(
        setup,
        text="Difficulty:",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(
        pady=(15, 5)
    )

    multi_difficulty_var = (
        tk.StringVar(
            value=difficulty_var.get()
        )
    )

    difficulty_menu = tk.OptionMenu(
        setup,
        multi_difficulty_var,
        "Easy",
        "Medium",
        "Hard"
    )

    difficulty_menu.pack()

    def start_multiplayer():

        names = []

        for entry in entries:

            name = (
                entry.get().strip()
            )

            if name:
                names.append(name)

        if len(names) < 2:

            messagebox.showwarning(
                "Players Required",
                "Enter at least 2 players."
            )

            return

        if len(set(names)) != len(names):

            messagebox.showwarning(
                "Duplicate Names",
                "Player names must be unique."
            )

            return

        rounds = rounds_var.get()

        start_multiplayer_game(
            names,
            rounds,
            multi_difficulty_var.get()
        )

        setup.destroy()

    tk.Button(
        setup,
        text="🚀 START MULTIPLAYER",
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        command=start_multiplayer,
        padx=20,
        pady=10
    ).pack(
        pady=30
    )


# ============================================================
# MULTIPLAYER START
# ============================================================

def start_multiplayer_game(
    names,
    rounds,
    difficulty
):

    global multiplayer_mode
    global multiplayer_players
    global multiplayer_scores
    global multiplayer_round
    global multiplayer_total_rounds
    global current_player_index
    global multiplayer_secret
    global multiplayer_attempts
    global minimum
    global maximum
    global max_attempts
    global current_multiplier
    global multiplayer_game_active

    multiplayer_mode = True

    multiplayer_players = names

    multiplayer_scores = {
        name: 0
        for name in names
    }

    multiplayer_round = 1

    multiplayer_total_rounds = rounds

    current_player_index = 0

    settings = (
        DIFFICULTY_SETTINGS[
            difficulty
        ]
    )

    minimum = settings[
        "minimum"
    ]

    maximum = settings[
        "maximum"
    ]

    max_attempts = settings[
        "attempts"
    ]

    current_multiplier = settings[
        "multiplier"
    ]

    difficulty_var.set(
        difficulty
    )

    multiplayer_secret = random.randint(
        minimum,
        maximum
    )

    multiplayer_attempts = 0

    multiplayer_game_active = True

    stop_timer()

    guess_entry.delete(
        0,
        tk.END
    )

    update_multiplayer_display()

    multiplayer_window()


# ============================================================
# MULTIPLAYER DISPLAY
# ============================================================

def update_multiplayer_display():

    if not multiplayer_players:
        return

    current_player = (
        multiplayer_players[
            current_player_index
        ]
    )

    result_label.config(
        text=(
            f"👥 Round "
            f"{multiplayer_round} / "
            f"{multiplayer_total_rounds}\n\n"
            f"🎮 Current Player: "
            f"{current_player}\n\n"
            f"Guess between "
            f"{minimum} and {maximum}."
        )
    )

    attempts_value.config(
        text=(
            f"{multiplayer_attempts} / "
            f"{max_attempts}"
        )
    )

    score_value.config(
        text=str(
            multiplayer_scores[
                current_player
            ]
        )
    )

    multiplier_value.config(
        text=f"{current_multiplier}×"
    )

    timer_value.config(
        text="MULTI"
    )


# ============================================================
# MULTIPLAYER GUESS
# ============================================================

def check_multiplayer_guess():

    global multiplayer_attempts

    if not multiplayer_game_active:
        return

    try:

        guess = int(
            guess_entry.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter a valid number."
        )

        return

    if (
        guess < minimum
        or
        guess > maximum
    ):

        messagebox.showwarning(
            "Out of Range",
            f"Enter a number between "
            f"{minimum} and {maximum}."
        )

        return

    multiplayer_attempts += 1

    current_player = (
        multiplayer_players[
            current_player_index
        ]
    )

    attempts_value.config(
        text=(
            f"{multiplayer_attempts} / "
            f"{max_attempts}"
        )
    )

    if guess < multiplayer_secret:

        play_sound(
            "low"
        )

        result_label.config(
            text=(
                f"⬇️ {current_player}, "
                f"TOO LOW!"
            )
        )

    elif guess > multiplayer_secret:

        play_sound(
            "high"
        )

        result_label.config(
            text=(
                f"⬆️ {current_player}, "
                f"TOO HIGH!"
            )
        )

    else:

        play_sound(
            "win"
        )

        points = (

            max(
                1,
                max_attempts
                - multiplayer_attempts
                + 1
            )
            * current_multiplier
        )

        multiplayer_scores[
            current_player
        ] += points

        score_value.config(
            text=str(
                multiplayer_scores[
                    current_player
                ]
            )
        )

        messagebox.showinfo(
            "🎉 Correct!",
            f"{current_player} "
            f"found the number!\n\n"
            f"Number: "
            f"{multiplayer_secret}\n"
            f"Points: {points}"
        )

        next_multiplayer_turn()

        return

    if (
        multiplayer_attempts
        >= max_attempts
    ):

        messagebox.showinfo(
            "Round Over",
            f"{current_player} "
            f"ran out of attempts.\n\n"
            f"The number was "
            f"{multiplayer_secret}."
        )

        next_multiplayer_turn()


# ============================================================
# NEXT MULTIPLAYER TURN
# ============================================================

def next_multiplayer_turn():

    global current_player_index
    global multiplayer_round
    global multiplayer_secret
    global multiplayer_attempts

    guess_entry.delete(
        0,
        tk.END
    )

    current_player_index += 1

    if (
        current_player_index
        >= len(multiplayer_players)
    ):

        current_player_index = 0

        multiplayer_round += 1

    if (
        multiplayer_round
        > multiplayer_total_rounds
    ):

        finish_multiplayer_game()

        return

    multiplayer_secret = random.randint(
        minimum,
        maximum
    )

    multiplayer_attempts = 0

    update_multiplayer_display()


# ============================================================
# MULTIPLAYER SCOREBOARD
# ============================================================

def multiplayer_window():

    global multi_score_window

    try:

        if multi_score_window.winfo_exists():

            multi_score_window.destroy()

    except NameError:

        pass

    multi_score_window = tk.Toplevel(
        root
    )

    multi_score_window.title(
        "🏆 Live Scoreboard"
    )

    multi_score_window.geometry(
        "650x500"
    )

    background = (
        DARK_BG
        if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG
        if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME
        if dark_mode
        else LIGHT_FRAME
    )

    multi_score_window.config(
        bg=background
    )

    tk.Label(
        multi_score_window,
        text="🏆 LIVE SCOREBOARD",
        font=(
            "Segoe UI",
            24,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(
        pady=25
    )

    table = tk.Frame(
        multi_score_window,
        bg=frame_background
    )

    table.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    headers = [
        "Rank",
        "Player",
        "Score"
    ]

    for column, header in enumerate(
        headers
    ):

        tk.Label(
            table,
            text=header,
            font=(
                "Segoe UI",
                11,
                "bold"
            ),
            bg=frame_background,
            fg=foreground,
            width=15
        ).grid(
            row=0,
            column=column,
            padx=5,
            pady=15
        )

    sorted_players = sorted(
        multiplayer_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    for index, (
        name,
        player_score
    ) in enumerate(
        sorted_players,
        start=1
    ):

        if index == 1:
            rank = "🥇"

        elif index == 2:
            rank = "🥈"

        elif index == 3:
            rank = "🥉"

        else:
            rank = str(index)

        values = [
            rank,
            name,
            str(player_score)
        ]

        for column, value in enumerate(
            values
        ):

            tk.Label(
                table,
                text=value,
                font=(
                    "Segoe UI",
                    12,
                    "bold"
                ),
                bg=frame_background,
                fg=foreground,
                width=15
            ).grid(
                row=index,
                column=column,
                padx=5,
                pady=10
            )

    tk.Label(
        multi_score_window,
        text=(
            f"Round "
            f"{multiplayer_round} / "
            f"{multiplayer_total_rounds}"
        ),
        font=(
            "Segoe UI",
            11,
            "bold"
        ),
        bg=background,
        fg=foreground
    ).pack(
        pady=10
    )


# ============================================================
# MULTIPLAYER FINISH
# ============================================================

def finish_multiplayer_game():

    global multiplayer_game_active
    global multiplayer_mode

    multiplayer_game_active = False

    multiplayer_mode = False

    try:

        multi_score_window.destroy()

    except:

        pass

    sorted_players = sorted(
        multiplayer_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    winner_name = (
        sorted_players[0][0]
    )

    winner_score = (
        sorted_players[0][1]
    )

    result_text = (
        "🏆 MULTIPLAYER RESULTS\n\n"
    )

    for index, (
        name,
        player_score
    ) in enumerate(
        sorted_players,
        start=1
    ):

        result_text += (
            f"{index}. "
            f"{name} — "
            f"{player_score} points\n"
        )

    result_text += (
        f"\n🥇 Winner: "
        f"{winner_name}\n"
        f"🏆 Score: "
        f"{winner_score}"
    )

    result_label.config(
        text=(
            "🏆 MULTIPLAYER COMPLETE!\n"
            f"Winner: {winner_name}"
        )
    )

    play_sound(
        "win"
    )

    messagebox.showinfo(
        "🏆 Results",
        result_text
    )


# ============================================================
# RESET DATA
# ============================================================

def reset_data():

    global games_played
    global games_won
    global games_lost
    global best_score
    global winning_streak
    global game_history
    global leaderboard
    global fastest_win
    global highest_difficulty

    confirmation = messagebox.askyesno(
        "Reset Game Data",
        "Delete all statistics,\n"
        "history, leaderboard and "
        "achievements?"
    )

    if not confirmation:
        return

    stop_timer()

    games_played = 0

    games_won = 0

    games_lost = 0

    best_score = 0

    winning_streak = 0

    fastest_win = None

    highest_difficulty = "None"

    game_history = []

    leaderboard = []

    for difficulty in (
        difficulty_statistics
    ):

        difficulty_statistics[
            difficulty
        ] = {

            "played": 0,

            "won": 0,

            "lost": 0,

            "total_score": 0,

            "total_attempts": 0
        }

    for achievement in achievements:

        achievements[
            achievement
        ] = False

    save_data()

    update_dashboard()

    result_label.config(
        text=(
            "All game data "
            "has been cleared."
        )
    )

    attempts_value.config(
        text=(
            f"0 / {max_attempts}"
        )
    )

    score_value.config(
        text="0"
    )

    timer_value.config(
        text="00:00"
    )

    messagebox.showinfo(
        "Data Reset",
        "All game data "
        "has been cleared."
    )


# ============================================================
# DARK MODE
# ============================================================

def toggle_dark_mode():

    global dark_mode

    dark_mode = not dark_mode

    apply_theme()


def update_widget_colors(
    widget,
    foreground,
    frame_background,
    button_background
):

    for child in widget.winfo_children():

        try:

            if isinstance(
                child,
                tk.Button
            ):

                child.config(
                    bg=button_background,
                    fg=foreground,
                    activebackground=
                    button_background,
                    activeforeground=
                    foreground
                )

            elif isinstance(
                child,
                tk.Entry
            ):

                child.config(
                    bg=frame_background,
                    fg=foreground,
                    insertbackground=
                    foreground
                )

            elif isinstance(
                child,
                tk.Label
            ):

                child.config(
                    bg=frame_background,
                    fg=foreground
                )

            elif isinstance(
                child,
                tk.Frame
            ):

                child.config(
                    bg=frame_background
                )

        except tk.TclError:

            pass

        update_widget_colors(
            child,
            foreground,
            frame_background,
            button_background
        )


def apply_theme():

    if dark_mode:

        background = DARK_BG

        foreground = DARK_FG

        frame_background = (
            DARK_FRAME
        )

        button_background = (
            DARK_BUTTON
        )

        theme_button.config(
            text="☀️ LIGHT MODE"
        )

    else:

        background = LIGHT_BG

        foreground = LIGHT_FG

        frame_background = (
            LIGHT_FRAME
        )

        button_background = (
            LIGHT_BUTTON
        )

        theme_button.config(
            text="🌙 DARK MODE"
        )

    root.config(
        bg=background
    )

    header.config(
        bg=background
    )

    player_frame.config(
        bg=frame_background,
        fg=foreground
    )

    mode_frame.config(
        bg=frame_background,
        fg=foreground
    )

    stats_frame.config(
        bg=frame_background,
        fg=foreground
    )

    game_frame.config(
        bg=frame_background,
        fg=foreground
    )

    action_frame.config(
        bg=background
    )

    footer_label.config(
        bg=background,
        fg=foreground
    )

    mode_info_label.config(
        bg=frame_background,
        fg=foreground
    )

    update_widget_colors(
        root,
        foreground,
        frame_background,
        button_background
    )

    update_sound_button()


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Number Guessing Game | V18"
)

root.geometry(
    "1150x1150"
)

root.resizable(
    False,
    False
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    padx=30,
    pady=20
)

header.pack(
    fill="x"
)


title_label = tk.Label(
    header,
    text=(
        "🎯 Number Guessing Game"
    ),
    font=(
        "Segoe UI",
        26,
        "bold"
    )
)

title_label.pack(
    side="left"
)


subtitle_label = tk.Label(
    header,
    text=(
        "V18 • Custom Modes • "
        "Multiplayer • Profiles"
    ),
    font=(
        "Segoe UI",
        11
    )
)

subtitle_label.pack(
    side="right",
    pady=10
)


# ============================================================
# PLAYER SETUP
# ============================================================

player_frame = tk.LabelFrame(
    root,
    text="  👤 Player Setup  ",
    font=(
        "Segoe UI",
        12,
        "bold"
    ),
    padx=20,
    pady=15
)

player_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Label(
    player_frame,
    text="Player Name:",
    font=(
        "Segoe UI",
        11,
        "bold"
    )
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)


name_entry = tk.Entry(
    player_frame,
    font=(
        "Segoe UI",
        11
    ),
    width=20
)

name_entry.grid(
    row=0,
    column=1,
    padx=10
)


tk.Label(
    player_frame,
    text="Difficulty:",
    font=(
        "Segoe UI",
        11,
        "bold"
    )
).grid(
    row=0,
    column=2,
    padx=10
)


difficulty_var = tk.StringVar(
    value="Medium"
)


difficulty_menu = tk.OptionMenu(
    player_frame,
    difficulty_var,
    "Easy",
    "Medium",
    "Hard"
)

difficulty_menu.config(
    font=(
        "Segoe UI",
        10
    ),
    width=10
)

difficulty_menu.grid(
    row=0,
    column=3,
    padx=10
)


start_button = tk.Button(
    player_frame,
    text="START GAME",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=start_player_game,
    padx=15,
    pady=5
)

start_button.grid(
    row=0,
    column=4,
    padx=15
)


multiplayer_button = tk.Button(
    player_frame,
    text="👥 MULTIPLAYER",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=show_multiplayer_setup,
    padx=15,
    pady=5
)

multiplayer_button.grid(
    row=0,
    column=5,
    padx=10
)


# ============================================================
# V18 GAME MODE
# ============================================================

mode_frame = tk.LabelFrame(
    root,
    text="  🎮 V18 Game Mode  ",
    font=(
        "Segoe UI",
        12,
        "bold"
    ),
    padx=20,
    pady=15
)

mode_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


tk.Label(
    mode_frame,
    text="Select Mode:",
    font=(
        "Segoe UI",
        11,
        "bold"
    )
).grid(
    row=0,
    column=0,
    padx=10
)


mode_var = tk.StringVar(
    value="Classic Mode"
)


mode_menu = tk.OptionMenu(
    mode_frame,
    mode_var,
    *GAME_MODES,
    command=lambda _: change_game_mode()
)

mode_menu.config(
    font=(
        "Segoe UI",
        10
    ),
    width=18
)

mode_menu.grid(
    row=0,
    column=1,
    padx=10
)


mode_info_label = tk.Label(
    mode_frame,
    text=(
        "Normal number guessing."
    ),
    font=(
        "Segoe UI",
        10
    )
)

mode_info_label.grid(
    row=0,
    column=2,
    padx=20
)


# ============================================================
# STATISTICS
# ============================================================

stats_frame = tk.LabelFrame(
    root,
    text="  📊 Your Statistics  ",
    font=(
        "Segoe UI",
        12,
        "bold"
    ),
    padx=15,
    pady=15
)

stats_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


def create_stat_card(
    parent,
    title,
    value,
    column
):

    frame = tk.Frame(
        parent,
        padx=20,
        pady=10
    )

    frame.grid(
        row=0,
        column=column,
        padx=8
    )

    tk.Label(
        frame,
        text=title,
        font=(
            "Segoe UI",
            10
        )
    ).pack()

    value_label = tk.Label(
        frame,
        text=str(value),
        font=(
            "Segoe UI",
            21,
            "bold"
        )
    )

    value_label.pack()

    return value_label


played_value = create_stat_card(
    stats_frame,
    "Games Played",
    games_played,
    0
)

won_value = create_stat_card(
    stats_frame,
    "Games Won",
    games_won,
    1
)

lost_value = create_stat_card(
    stats_frame,
    "Games Lost",
    games_lost,
    2
)

best_value = create_stat_card(
    stats_frame,
    "Best Score",
    best_score,
    3
)


# ============================================================
# GAME AREA
# ============================================================

game_frame = tk.LabelFrame(
    root,
    text="  🎮 Current Game  ",
    font=(
        "Segoe UI",
        12,
        "bold"
    ),
    padx=30,
    pady=20
)

game_frame.pack(
    fill="x",
    padx=30,
    pady=10
)


result_label = tk.Label(
    game_frame,
    text=(
        "Enter your name "
        "and start a game."
    ),
    font=(
        "Segoe UI",
        14,
        "bold"
    ),
    wraplength=900,
    justify="center"
)

result_label.pack(
    pady=10
)


guess_entry = tk.Entry(
    game_frame,
    font=(
        "Segoe UI",
        20
    ),
    justify="center",
    width=12
)

guess_entry.pack(
    pady=10
)


guess_button = tk.Button(
    game_frame,
    text="GUESS",
    font=(
        "Segoe UI",
        12,
        "bold"
    ),
    command=check_guess,
    width=15,
    pady=8
)

guess_button.pack(
    pady=10
)


# ============================================================
# GAME INFORMATION
# ============================================================

info_frame = tk.Frame(
    game_frame
)

info_frame.pack(
    pady=10
)


labels = [
    "Attempts",
    "Score",
    "Multiplier",
    "Time"
]

for column, text in enumerate(
    labels
):

    tk.Label(
        info_frame,
        text=text,
        font=(
            "Segoe UI",
            10
        )
    ).grid(
        row=0,
        column=column,
        padx=30
    )


attempts_value = tk.Label(
    info_frame,
    text="0 / 10",
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

attempts_value.grid(
    row=1,
    column=0,
    padx=30
)


score_value = tk.Label(
    info_frame,
    text="0",
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

score_value.grid(
    row=1,
    column=1,
    padx=30
)


multiplier_value = tk.Label(
    info_frame,
    text="2×",
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

multiplier_value.grid(
    row=1,
    column=2,
    padx=30
)


timer_value = tk.Label(
    info_frame,
    text="00:00",
    font=(
        "Segoe UI",
        16,
        "bold"
    )
)

timer_value.grid(
    row=1,
    column=3,
    padx=30
)


# ============================================================
# ACTION BUTTONS
# ============================================================

action_frame = tk.Frame(
    root
)

action_frame.pack(
    pady=15
)


new_game_button = tk.Button(
    action_frame,
    text="🔄 NEW GAME",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=start_new_game,
    width=18,
    pady=8
)

new_game_button.grid(
    row=0,
    column=0,
    padx=5
)


profile_button = tk.Button(
    action_frame,
    text="👤 PLAYER PROFILE",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=show_profile,
    width=18,
    pady=8
)

profile_button.grid(
    row=0,
    column=1,
    padx=5
)


history_button = tk.Button(
    action_frame,
    text="📜 GAME HISTORY",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=show_history,
    width=18,
    pady=8
)

history_button.grid(
    row=0,
    column=2,
    padx=5
)


leaderboard_button = tk.Button(
    action_frame,
    text="🏆 LEADERBOARD",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=show_leaderboard,
    width=18,
    pady=8
)

leaderboard_button.grid(
    row=0,
    column=3,
    padx=5
)


achievement_button = tk.Button(
    action_frame,
    text="🏅 ACHIEVEMENTS",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=show_achievements,
    width=18,
    pady=8
)

achievement_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=8
)


reset_button = tk.Button(
    action_frame,
    text="🗑️ RESET DATA",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=reset_data,
    width=18,
    pady=8
)

reset_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=8
)


theme_button = tk.Button(
    action_frame,
    text="🌙 DARK MODE",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=toggle_dark_mode,
    width=18,
    pady=8
)

theme_button.grid(
    row=1,
    column=2,
    padx=5,
    pady=8
)


sound_button = tk.Button(
    action_frame,
    text="🔊 SOUND ON",
    font=(
        "Segoe UI",
        10,
        "bold"
    ),
    command=toggle_sound,
    width=18,
    pady=8
)

sound_button.grid(
    row=1,
    column=3,
    padx=5,
    pady=8
)


# ============================================================
# FOOTER
# ============================================================

footer_label = tk.Label(
    root,
    text=(
        "V18 • Custom Game Modes • "
        "Multiplayer • Profiles • "
        "Statistics • Leaderboard • "
        "Achievements • Timer • "
        "Sound • Dynamic Scoring"
    ),
    font=(
        "Segoe UI",
        9
    )
)

footer_label.pack(
    pady=5
)


# ============================================================
# INITIAL THEME
# ============================================================

apply_theme()


# ============================================================
# RUN APPLICATION
# ============================================================

root.mainloop()