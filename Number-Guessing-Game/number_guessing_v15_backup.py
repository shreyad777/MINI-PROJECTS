import tkinter as tk
from tkinter import messagebox
import random
import json
import os
import winsound


# ============================================================
# FILE
# ============================================================

DATA_FILE = "game_data.json"


# ============================================================
# GAME VARIABLES
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

game_history = []
leaderboard = []

winning_streak = 0

# Timer
game_active = False
timer_seconds = 0
timer_job = None

# Theme
dark_mode = False

# Sound
sound_enabled = True


# ============================================================
# ACHIEVEMENTS
# ============================================================

achievements = {
    "First Victory": False,
    "Winning Streak": False,
    "Speed Demon": False,
    "Perfect Guesser": False,
    "Score Master": False,
    "Leaderboard Champion": False
}


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


current_multiplier = 2


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
# SOUND SYSTEM
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

        sound_button.config(
            text="🔊 SOUND ON"
        )

    else:

        sound_button.config(
            text="🔇 SOUND OFF"
        )


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not os.path.exists(DATA_FILE):

        return (
            0,
            0,
            0,
            0,
            [],
            [],
            0,
            True,
            {}
        )

    try:

        with open(DATA_FILE, "r") as file:

            data = json.load(file)

        saved_achievements = data.get(
            "achievements",
            {}
        )

        for achievement in achievements:

            if achievement in saved_achievements:

                achievements[achievement] = (
                    saved_achievements[achievement]
                )

        return (
            data.get("games_played", 0),
            data.get("games_won", 0),
            data.get("games_lost", 0),
            data.get("best_score", 0),
            data.get("game_history", []),
            data.get("leaderboard", []),
            data.get("winning_streak", 0),
            data.get("sound_enabled", True),
            saved_achievements
        )

    except (json.JSONDecodeError, OSError):

        return (
            0,
            0,
            0,
            0,
            [],
            [],
            0,
            True,
            {}
        )


(
    games_played,
    games_won,
    games_lost,
    best_score,
    game_history,
    leaderboard,
    winning_streak,
    sound_enabled,
    saved_achievements
) = load_data()


# ============================================================
# SAVE DATA
# ============================================================

def save_data():

    data = {

        "games_played": games_played,

        "games_won": games_won,

        "games_lost": games_lost,

        "best_score": best_score,

        "game_history": game_history,

        "leaderboard": leaderboard,

        "achievements": achievements,

        "winning_streak": winning_streak,

        "sound_enabled": sound_enabled
    }

    try:

        with open(DATA_FILE, "w") as file:

            json.dump(
                data,
                file,
                indent=4
            )

    except OSError:

        print("Unable to save game data.")


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

    difficulty = difficulty_var.get()

    settings = DIFFICULTY_SETTINGS[difficulty]

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

    return f"{minutes:02d}:{remaining_seconds:02d}"


def update_timer():

    global timer_seconds
    global timer_job

    if not game_active:

        return

    timer_seconds += 1

    timer_value.config(
        text=format_time(timer_seconds)
    )

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
# PLAYER
# ============================================================

def start_player_game():

    global player_name

    player_name = name_entry.get().strip()

    if not player_name:

        messagebox.showwarning(
            "Name Required",
            "Please enter your name."
        )

        return

    set_difficulty()


# ============================================================
# NEW GAME
# ============================================================

def start_new_game():

    global secret_number
    global attempts
    global score

    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Please enter your name first."
        )

        return

    stop_timer()

    secret_number = random.randint(
        minimum,
        maximum
    )

    attempts = 0

    score = 0

    guess_entry.delete(
        0,
        tk.END
    )

    difficulty = difficulty_var.get()

    result_label.config(
        text=(
            f"Welcome, {player_name}!\n"
            f"{difficulty} Mode\n"
            f"Guess a number between "
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
# SCORE CALCULATION
# ============================================================

def calculate_score():

    remaining_attempts = (
        max_attempts - attempts + 1
    )

    base_score = (
        remaining_attempts * current_multiplier
    )

    time_bonus = 0

    if timer_seconds <= 10:

        time_bonus = 5

    elif timer_seconds <= 20:

        time_bonus = 3

    elif timer_seconds <= 30:

        time_bonus = 1

    final_score = (
        base_score + time_bonus
    )

    return final_score


# ============================================================
# ACHIEVEMENTS
# ============================================================

def unlock_achievement(name):

    if achievements.get(name, False):

        return False

    achievements[name] = True

    play_sound("achievement")

    save_data()

    return True


def check_achievements(final_score):

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


def add_to_leaderboard(final_score):

    if final_score <= 0:

        return

    entry = {

        "player": player_name,

        "score": final_score,

        "time": format_time(
            timer_seconds
        ),

        "time_seconds": timer_seconds,

        "difficulty": difficulty_var.get()
    }

    leaderboard.append(
        entry
    )

    update_leaderboard()


def show_leaderboard():

    window = tk.Toplevel(root)

    window.title(
        "🏆 Leaderboard"
    )

    window.geometry(
        "800x600"
    )

    background = (
        DARK_BG if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="🏆 LEADERBOARD",
        font=("Segoe UI", 24, "bold"),
        bg=background,
        fg=foreground
    ).pack(
        pady=20
    )

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
        "Difficulty"
    ]

    for column, header in enumerate(headers):

        tk.Label(
            table,
            text=header,
            font=("Segoe UI", 11, "bold"),
            bg=frame_background,
            fg=foreground,
            width=15
        ).grid(
            row=0,
            column=column,
            padx=5,
            pady=12
        )

    if not leaderboard:

        tk.Label(
            table,
            text="No winning games yet.",
            font=("Segoe UI", 13),
            bg=frame_background,
            fg=foreground
        ).grid(
            row=1,
            column=0,
            columnspan=5,
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

            entry["difficulty"]
        ]

        for column, value in enumerate(values):

            tk.Label(
                table,
                text=value,
                font=("Segoe UI", 11),
                bg=frame_background,
                fg=foreground,
                width=15
            ).grid(
                row=index,
                column=column,
                padx=5,
                pady=8
            )


# ============================================================
# ACHIEVEMENT WINDOW
# ============================================================

def show_achievements():

    window = tk.Toplevel(root)

    window.title(
        "🏅 Achievements"
    )

    window.geometry(
        "700x650"
    )

    background = (
        DARK_BG if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="🏅 ACHIEVEMENTS",
        font=("Segoe UI", 25, "bold"),
        bg=background,
        fg=foreground
    ).pack(
        pady=(25, 5)
    )

    tk.Label(
        window,
        text="Complete challenges and collect badges!",
        font=("Segoe UI", 11),
        bg=background,
        fg=foreground
    ).pack(
        pady=(0, 20)
    )

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
        "Reach #1 on the leaderboard."
    }

    icons = {

        "First Victory": "🏆",

        "Winning Streak": "🔥",

        "Speed Demon": "⚡",

        "Perfect Guesser": "🎯",

        "Score Master": "💯",

        "Leaderboard Champion": "🥇"
    }

    for name in achievements:

        unlocked = achievements[name]

        if unlocked:

            title = (
                f"{icons[name]} {name}"
            )

            status = "✅ UNLOCKED"

        else:

            title = (
                f"🔒 {name}"
            )

            status = "🔒 LOCKED"

        frame = tk.Frame(
            container,
            bg=frame_background,
            padx=15,
            pady=10
        )

        frame.pack(
            fill="x",
            padx=20,
            pady=6
        )

        tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 12, "bold"),
            bg=frame_background,
            fg=foreground,
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Label(
            frame,
            text=badge_details[name],
            font=("Segoe UI", 10),
            bg=frame_background,
            fg=foreground,
            anchor="w"
        ).pack(
            fill="x"
        )

        tk.Label(
            frame,
            text=status,
            font=("Segoe UI", 9, "bold"),
            bg=frame_background,
            fg=foreground,
            anchor="w"
        ).pack(
            fill="x"
        )


# ============================================================
# HISTORY
# ============================================================

def add_history(result, final_score):

    record = {

        "player": player_name,

        "difficulty": difficulty_var.get(),

        "result": result,

        "attempts": attempts,

        "score": final_score,

        "time": format_time(
            timer_seconds
        )
    }

    game_history.append(
        record
    )

    save_data()


def show_history():

    window = tk.Toplevel(root)

    window.title(
        "📜 Game History"
    )

    window.geometry(
        "750x600"
    )

    background = (
        DARK_BG if dark_mode
        else LIGHT_BG
    )

    foreground = (
        DARK_FG if dark_mode
        else LIGHT_FG
    )

    frame_background = (
        DARK_FRAME if dark_mode
        else LIGHT_FRAME
    )

    window.config(
        bg=background
    )

    tk.Label(
        window,
        text="📜 GAME HISTORY",
        font=("Segoe UI", 22, "bold"),
        bg=background,
        fg=foreground
    ).pack(
        pady=20
    )

    if not game_history:

        tk.Label(
            window,
            text="No games played yet.",
            font=("Segoe UI", 13),
            bg=background,
            fg=foreground
        ).pack(
            pady=50
        )

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
        font=("Consolas", 11),
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
            f"Player     : {game['player']}\n"
        )

        text.insert(
            tk.END,
            f"Difficulty : {game['difficulty']}\n"
        )

        text.insert(
            tk.END,
            f"Result     : {game['result']}\n"
        )

        text.insert(
            tk.END,
            f"Attempts   : {game['attempts']}\n"
        )

        text.insert(
            tk.END,
            f"Score      : {game['score']}\n"
        )

        text.insert(
            tk.END,
            f"Time       : {game.get('time', '00:00')}\n"
        )

        text.insert(
            tk.END,
            "-" * 55 + "\n\n"
        )

    text.config(
        state="disabled"
    )


# ============================================================
# RESET DATA
# ============================================================

def reset_data():

    global games_played
    global games_won
    global games_lost
    global best_score
    global game_history
    global leaderboard
    global winning_streak

    confirmation = messagebox.askyesno(
        "Reset Game Data",
        "Delete all statistics, history,\n"
        "leaderboard and achievements?"
    )

    if not confirmation:

        return

    stop_timer()

    games_played = 0
    games_won = 0
    games_lost = 0
    best_score = 0
    winning_streak = 0

    game_history = []
    leaderboard = []

    for achievement in achievements:

        achievements[achievement] = False

    save_data()

    update_dashboard()

    result_label.config(
        text="All game data has been cleared."
    )

    attempts_value.config(
        text=f"0 / {max_attempts}"
    )

    score_value.config(
        text="0"
    )

    timer_value.config(
        text="00:00"
    )

    messagebox.showinfo(
        "Data Reset",
        "All game data has been cleared."
    )


# ============================================================
# CHECK GUESS
# ============================================================

def check_guess():

    global attempts
    global score
    global best_score
    global games_played
    global games_won
    global games_lost
    global winning_streak

    if not player_name:

        messagebox.showwarning(
            "Start Game",
            "Enter your name and start a game first."
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

    if guess < minimum or guess > maximum:

        messagebox.showwarning(
            "Out of Range",
            f"Enter a number between "
            f"{minimum} and {maximum}."
        )

        return

    attempts += 1

    attempts_value.config(
        text=f"{attempts} / {max_attempts}"
    )

    if guess < secret_number:

        play_sound("low")

        result_label.config(
            text="⬇️ Too low! Try again."
        )

    elif guess > secret_number:

        play_sound("high")

        result_label.config(
            text="⬆️ Too high! Try again."
        )

    else:

        stop_timer()

        play_sound("win")

        score = calculate_score()

        games_played += 1

        games_won += 1

        winning_streak += 1

        if score > best_score:

            best_score = score

        score_value.config(
            text=str(score)
        )

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

        update_dashboard()

        result_label.config(
            text=(
                f"🎉 Congratulations, "
                f"{player_name}!\n"
                f"You found the number!"
            )
        )

        achievement_message = ""

        if unlocked:

            achievement_message = (
                "\n\n🏅 NEW ACHIEVEMENTS!\n"
                + "\n".join(unlocked)
            )

        messagebox.showinfo(
            "🎉 You Won!",
            f"Player: {player_name}\n\n"
            f"Difficulty: {difficulty_var.get()}\n"
            f"Attempts: {attempts}\n"
            f"Score: {score}\n"
            f"Multiplier: {current_multiplier}×\n"
            f"Time: {format_time(timer_seconds)}\n"
            f"Winning Streak: {winning_streak}\n"
            f"Best Score: {best_score}"
            f"{achievement_message}"
        )

        return

    if attempts >= max_attempts:

        stop_timer()

        play_sound("lose")

        games_played += 1

        games_lost += 1

        winning_streak = 0

        add_history(
            "Lost",
            0
        )

        update_dashboard()

        save_data()

        result_label.config(
            text=(
                f"❌ Game Over!\n"
                f"The number was "
                f"{secret_number}."
            )
        )

        messagebox.showinfo(
            "❌ Game Over",
            f"Better luck next time!\n\n"
            f"The number was {secret_number}.\n"
            f"Difficulty: {difficulty_var.get()}\n"
            f"Time: {format_time(timer_seconds)}"
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
                    activebackground=button_background,
                    activeforeground=foreground
                )

            elif isinstance(
                child,
                tk.Entry
            ):

                child.config(
                    bg=frame_background,
                    fg=foreground,
                    insertbackground=foreground
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
                tk.OptionMenu
            ):

                child.config(
                    bg=button_background,
                    fg=foreground,
                    activebackground=button_background,
                    activeforeground=foreground
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
        frame_background = DARK_FRAME
        button_background = DARK_BUTTON

        theme_button.config(
            text="☀️ LIGHT MODE"
        )

    else:

        background = LIGHT_BG
        foreground = LIGHT_FG
        frame_background = LIGHT_FRAME
        button_background = LIGHT_BUTTON

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
    "Number Guessing Game | V15"
)

root.geometry(
    "1100x980"
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
    text="🎯 Number Guessing Game",
    font=("Segoe UI", 26, "bold")
)

title_label.pack(
    side="left"
)


subtitle_label = tk.Label(
    header,
    text="Choose your difficulty • Earn more points • Beat the leaderboard",
    font=("Segoe UI", 11)
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
    font=("Segoe UI", 12, "bold"),
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
    font=("Segoe UI", 11, "bold")
).grid(
    row=0,
    column=0,
    padx=10,
    pady=5
)


name_entry = tk.Entry(
    player_frame,
    font=("Segoe UI", 11),
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
    font=("Segoe UI", 11, "bold")
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
    font=("Segoe UI", 10),
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
    font=("Segoe UI", 10, "bold"),
    command=start_player_game,
    padx=15,
    pady=5
)

start_button.grid(
    row=0,
    column=4,
    padx=15
)


# ============================================================
# STATISTICS
# ============================================================

stats_frame = tk.LabelFrame(
    root,
    text="  📊 Your Statistics  ",
    font=("Segoe UI", 12, "bold"),
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
        font=("Segoe UI", 10)
    ).pack()

    value_label = tk.Label(
        frame,
        text=str(value),
        font=("Segoe UI", 21, "bold")
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
    font=("Segoe UI", 12, "bold"),
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
    text="Enter your name and start a game.",
    font=("Segoe UI", 14, "bold"),
    wraplength=800,
    justify="center"
)

result_label.pack(
    pady=10
)


guess_entry = tk.Entry(
    game_frame,
    font=("Segoe UI", 20),
    justify="center",
    width=12
)

guess_entry.pack(
    pady=10
)


guess_button = tk.Button(
    game_frame,
    text="GUESS",
    font=("Segoe UI", 12, "bold"),
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


tk.Label(
    info_frame,
    text="Attempts",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=0,
    padx=30
)


tk.Label(
    info_frame,
    text="Score",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=1,
    padx=30
)


tk.Label(
    info_frame,
    text="Multiplier",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=2,
    padx=30
)


tk.Label(
    info_frame,
    text="Time",
    font=("Segoe UI", 10)
).grid(
    row=0,
    column=3,
    padx=30
)


attempts_value = tk.Label(
    info_frame,
    text="0 / 10",
    font=("Segoe UI", 16, "bold")
)

attempts_value.grid(
    row=1,
    column=0,
    padx=30
)


score_value = tk.Label(
    info_frame,
    text="0",
    font=("Segoe UI", 16, "bold")
)

score_value.grid(
    row=1,
    column=1,
    padx=30
)


multiplier_value = tk.Label(
    info_frame,
    text="2×",
    font=("Segoe UI", 16, "bold")
)

multiplier_value.grid(
    row=1,
    column=2,
    padx=30
)


timer_value = tk.Label(
    info_frame,
    text="00:00",
    font=("Segoe UI", 16, "bold")
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
    font=("Segoe UI", 10, "bold"),
    command=start_new_game,
    width=18,
    pady=8
)

new_game_button.grid(
    row=0,
    column=0,
    padx=5
)


history_button = tk.Button(
    action_frame,
    text="📜 GAME HISTORY",
    font=("Segoe UI", 10, "bold"),
    command=show_history,
    width=18,
    pady=8
)

history_button.grid(
    row=0,
    column=1,
    padx=5
)


leaderboard_button = tk.Button(
    action_frame,
    text="🏆 LEADERBOARD",
    font=("Segoe UI", 10, "bold"),
    command=show_leaderboard,
    width=18,
    pady=8
)

leaderboard_button.grid(
    row=0,
    column=2,
    padx=5
)


achievement_button = tk.Button(
    action_frame,
    text="🏅 ACHIEVEMENTS",
    font=("Segoe UI", 10, "bold"),
    command=show_achievements,
    width=18,
    pady=8
)

achievement_button.grid(
    row=0,
    column=3,
    padx=5
)


reset_button = tk.Button(
    action_frame,
    text="🗑️ RESET DATA",
    font=("Segoe UI", 10, "bold"),
    command=reset_data,
    width=18,
    pady=8
)

reset_button.grid(
    row=1,
    column=0,
    padx=5,
    pady=8
)


theme_button = tk.Button(
    action_frame,
    text="🌙 DARK MODE",
    font=("Segoe UI", 10, "bold"),
    command=toggle_dark_mode,
    width=18,
    pady=8
)

theme_button.grid(
    row=1,
    column=1,
    padx=5,
    pady=8
)


sound_button = tk.Button(
    action_frame,
    text="🔊 SOUND ON",
    font=("Segoe UI", 10, "bold"),
    command=toggle_sound,
    width=18,
    pady=8
)

sound_button.grid(
    row=1,
    column=2,
    padx=5,
    pady=8
)


# ============================================================
# FOOTER
# ============================================================

footer_label = tk.Label(
    root,
    text=(
        "Python • Tkinter • JSON • Timer • "
        "Leaderboard • Achievements • Sound • Dynamic Scoring"
    ),
    font=("Segoe UI", 9)
)

footer_label.pack(
    pady=5
)


# ============================================================
# START APPLICATION
# ============================================================

apply_theme()

root.mainloop()