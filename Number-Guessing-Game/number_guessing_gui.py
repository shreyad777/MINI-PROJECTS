import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# =========================================================
# NUMBER GUESSING GAME - V22
# MODERN CHALLENGE EDITION
# =========================================================

SAVE_FILE = "game_data_v22.json"

DIFFICULTIES = {
    "Easy": {
        "maximum": 50,
        "attempts": 15,
        "time": 90,
        "score": 100
    },
    "Medium": {
        "maximum": 100,
        "attempts": 10,
        "time": 60,
        "score": 200
    },
    "Hard": {
        "maximum": 500,
        "attempts": 7,
        "time": 45,
        "score": 300
    }
}

# =========================================================
# GLOBAL VARIABLES
# =========================================================

game_mode = "Single Player"
difficulty = "Medium"

player1_name = "Player 1"
player2_name = "Player 2"

secret_number = 0
current_player = 1

attempts_used = 0
max_attempts = 10

timer_seconds = 60
timer_running = False

player1_score = 0
player2_score = 0

player1_streak = 0
player2_streak = 0

hints_used = 0

dark_mode = True

games_played = 0
games_won = 0
best_score = 0
best_streak = 0

achievements = []


# =========================================================
# DATA MANAGEMENT
# =========================================================

def load_data():

    global games_played
    global games_won
    global best_score
    global best_streak
    global achievements

    if not os.path.exists(SAVE_FILE):
        return

    try:

        with open(SAVE_FILE, "r") as file:
            data = json.load(file)

        games_played = data.get("games_played", 0)
        games_won = data.get("games_won", 0)
        best_score = data.get("best_score", 0)
        best_streak = data.get("best_streak", 0)
        achievements = data.get("achievements", [])

    except (json.JSONDecodeError, OSError):
        pass


def save_data():

    data = {
        "games_played": games_played,
        "games_won": games_won,
        "best_score": best_score,
        "best_streak": best_streak,
        "achievements": achievements
    }

    try:

        with open(SAVE_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:
        pass


# =========================================================
# THEME
# =========================================================

def get_background():

    if dark_mode:
        return "#0f1117"

    return "#f4f6f8"


def get_card():

    if dark_mode:
        return "#1b1f2a"

    return "#ffffff"


def get_text():

    if dark_mode:
        return "#ffffff"

    return "#1c1c1c"


def toggle_theme():

    global dark_mode

    dark_mode = not dark_mode

    apply_theme()


def apply_theme():

    bg = get_background()
    card = get_card()
    text = get_text()

    root.configure(bg=bg)

    title_label.config(
        bg=bg,
        fg=text
    )

    subtitle_label.config(
        bg=bg
    )

    mode_label.config(
        bg=bg,
        fg=text
    )

    difficulty_label.config(
        bg=bg,
        fg=text
    )

    player_label.config(
        bg=bg,
        fg=text
    )

    range_frame.config(
        bg=card
    )

    range_label.config(
        bg=card,
        fg=text
    )

    result_label.config(
        bg=bg
    )

    score_label.config(
        bg=bg
    )

    attempts_label.config(
        bg=bg,
        fg=text
    )

    timer_label.config(
        bg=bg,
        fg=text
    )

    streak_label.config(
        bg=bg,
        fg=text
    )

    statistics_frame.config(
        bg=card
    )

    statistics_label.config(
        bg=card,
        fg=text
    )

    achievements_frame.config(
        bg=bg
    )

    achievements_label.config(
        bg=bg,
        fg=text
    )

    footer_label.config(
        bg=bg
    )


# =========================================================
# PLAYER NAME INPUT
# =========================================================

def set_player_names():

    global player1_name
    global player2_name

    name1 = player1_entry.get().strip()
    name2 = player2_entry.get().strip()

    if name1:
        player1_name = name1
    else:
        player1_name = "Player 1"

    if name2:
        player2_name = name2
    else:
        player2_name = "Player 2"

    if game_mode == "Single Player":

        player_label.config(
            text=f"👤 {player1_name}'S GAME"
        )

    else:

        player_label.config(
            text=f"👤 {player1_name}'S TURN"
        )

    messagebox.showinfo(
        "Players Updated",
        f"Player 1: {player1_name}\nPlayer 2: {player2_name}"
    )


# =========================================================
# GAME MODE
# =========================================================

def change_mode(value):

    global game_mode

    game_mode = value

    if game_mode == "Single Player":

        player2_entry.config(
            state=tk.DISABLED
        )

        player2_entry.delete(
            0,
            tk.END
        )

    else:

        player2_entry.config(
            state=tk.NORMAL
        )

    new_game()


# =========================================================
# DIFFICULTY
# =========================================================

def change_difficulty(value):

    global difficulty

    difficulty = value

    new_game()


# =========================================================
# NEW GAME
# =========================================================

def new_game():

    global secret_number
    global current_player
    global attempts_used
    global max_attempts
    global timer_seconds
    global timer_running
    global player1_score
    global player2_score
    global player1_streak
    global player2_streak
    global hints_used
    global games_played

    settings = DIFFICULTIES[difficulty]

    secret_number = random.randint(
        1,
        settings["maximum"]
    )

    current_player = 1

    attempts_used = 0
    max_attempts = settings["attempts"]

    timer_seconds = settings["time"]

    timer_running = True

    player1_score = settings["score"]
    player2_score = settings["score"]

    player1_streak = 0
    player2_streak = 0

    hints_used = 0

    games_played += 1

    result_label.config(
        text="🤔 A secret number has been generated.",
        fg=get_text()
    )

    range_label.config(
        text=f"Guess a number between 1 and {settings['maximum']}"
    )

    guess_entry.config(
        state=tk.NORMAL
    )

    guess_button.config(
        state=tk.NORMAL
    )

    hint_button.config(
        state=tk.NORMAL
    )

    guess_entry.delete(
        0,
        tk.END
    )

    guess_entry.focus()

    update_game_information()

    update_statistics()

    save_data()

    countdown()


# =========================================================
# GAME INFORMATION
# =========================================================

def update_game_information():

    if game_mode == "Single Player":

        player_label.config(
            text=f"👤 {player1_name}'S TURN",
            fg="#00bfff"
        )

        score_label.config(
            text=f"🏆 Score: {player1_score}"
        )

        streak_label.config(
            text=f"🔥 Streak: {player1_streak}"
        )

    else:

        if current_player == 1:

            player_label.config(
                text=f"👤 {player1_name.upper()}'S TURN",
                fg="#00bfff"
            )

        else:

            player_label.config(
                text=f"👤 {player2_name.upper()}'S TURN",
                fg="#ff77aa"
            )

        score_label.config(
            text=(
                f"🏆 {player1_name}: {player1_score}    "
                f"{player2_name}: {player2_score}"
            )
        )

        streak_label.config(
            text=(
                f"🔥 {player1_name}: {player1_streak}    "
                f"{player2_name}: {player2_streak}"
            )
        )

    attempts_label.config(
        text=f"🎯 Attempts: {attempts_used}/{max_attempts}"
    )

    timer_label.config(
        text=f"⏱️ Time: {timer_seconds}s"
    )


# =========================================================
# TIMER
# =========================================================

def countdown():

    global timer_seconds
    global timer_running

    if not timer_running:
        return

    if timer_seconds > 0:

        timer_seconds -= 1

        timer_label.config(
            text=f"⏱️ Time: {timer_seconds}s"
        )

        root.after(
            1000,
            countdown
        )

    else:

        timer_running = False

        game_over(
            "⏰ TIME'S UP!"
        )


# =========================================================
# HINT
# =========================================================

def use_hint():

    global hints_used
    global player1_score
    global player2_score

    if not timer_running:
        return

    if hints_used >= 3:

        messagebox.showwarning(
            "Hints",
            "You have already used all 3 hints."
        )

        return

    hints_used += 1

    if current_player == 1:

        player1_score = max(
            0,
            player1_score - 25
        )

    else:

        player2_score = max(
            0,
            player2_score - 25
        )

    if hints_used == 1:

        if secret_number % 2 == 0:

            hint = "💡 Hint: The number is EVEN."

        else:

            hint = "💡 Hint: The number is ODD."

    elif hints_used == 2:

        if secret_number <= 50:

            hint = "💡 Hint: The number is 50 or below."

        else:

            hint = "💡 Hint: The number is greater than 50."

    else:

        lower = max(
            1,
            secret_number - 10
        )

        upper = secret_number + 10

        hint = (
            f"💡 FINAL HINT\n"
            f"The number is between {lower} and {upper}."
        )

    result_label.config(
        text=hint,
        fg="#00bfff"
    )

    update_game_information()


# =========================================================
# CHECK GUESS
# =========================================================

def check_guess():

    global attempts_used
    global player1_score
    global player2_score
    global player1_streak
    global player2_streak
    global games_won
    global best_score
    global best_streak
    global timer_running
    global current_player

    if not timer_running:
        return

    value = guess_entry.get().strip()

    if not value:

        result_label.config(
            text="⚠️ Please enter a number."
        )

        return

    try:

        guess = int(value)

    except ValueError:

        result_label.config(
            text="❌ Please enter numbers only."
        )

        return

    maximum = DIFFICULTIES[difficulty]["maximum"]

    if guess < 1 or guess > maximum:

        result_label.config(
            text=f"⚠️ Enter a number from 1 to {maximum}."
        )

        return

    attempts_used += 1

    # =====================================================
    # CORRECT
    # =====================================================

    if guess == secret_number:

        timer_running = False

        games_won += 1

        remaining_attempts = (
            max_attempts - attempts_used
        )

        bonus = (
            remaining_attempts * 15
            + timer_seconds
            - hints_used * 25
        )

        bonus = max(
            10,
            bonus
        )

        if current_player == 1:

            player1_score += bonus

            player1_streak += 1

            if player1_score > best_score:
                best_score = player1_score

            if player1_streak > best_streak:
                best_streak = player1_streak

            winner = player1_name

        else:

            player2_score += bonus

            player2_streak += 1

            if player2_score > best_score:
                best_score = player2_score

            if player2_streak > best_streak:
                best_streak = player2_streak

            winner = player2_name

        result_label.config(
            text=(
                f"🎉 CORRECT!\n"
                f"{winner} wins!"
            ),
            fg="#00ff88"
        )

        update_game_information()

        guess_entry.config(
            state=tk.DISABLED
        )

        guess_button.config(
            state=tk.DISABLED
        )

        hint_button.config(
            state=tk.DISABLED
        )

        update_statistics()

        save_data()

        check_achievements()

        messagebox.showinfo(
            "🏆 WINNER!",
            (
                f"🎉 Congratulations, {winner}!\n\n"
                f"Secret Number: {secret_number}\n"
                f"Attempts: {attempts_used}\n"
                f"Score Earned: +{bonus}\n"
                f"Time Remaining: {timer_seconds}s"
            )
        )

        return

    # =====================================================
    # WRONG GUESS
    # =====================================================

    if current_player == 1:

        player1_score = max(
            0,
            player1_score - 10
        )

    else:

        player2_score = max(
            0,
            player2_score - 10
        )

    if guess < secret_number:

        result_label.config(
            text="📈 TOO LOW!\nTry a higher number.",
            fg="#ffaa00"
        )

    else:

        result_label.config(
            text="📉 TOO HIGH!\nTry a lower number.",
            fg="#ff7777"
        )

    guess_entry.delete(
        0,
        tk.END
    )

    # =====================================================
    # SWITCH PLAYER
    # =====================================================

    if (
        game_mode == "Two Player"
        and attempts_used < max_attempts
    ):

        current_player = (
            2 if current_player == 1 else 1
        )

    update_game_information()

    # =====================================================
    # ATTEMPTS EXHAUSTED
    # =====================================================

    if attempts_used >= max_attempts:

        game_over(
            "😢 NO ATTEMPTS LEFT!"
        )


# =========================================================
# GAME OVER
# =========================================================

def game_over(reason):

    global timer_running
    global player1_streak
    global player2_streak

    timer_running = False

    player1_streak = 0
    player2_streak = 0

    result_label.config(
        text=(
            f"{reason}\n"
            f"The number was {secret_number}"
        ),
        fg="#ff5555"
    )

    guess_entry.config(
        state=tk.DISABLED
    )

    guess_button.config(
        state=tk.DISABLED
    )

    hint_button.config(
        state=tk.DISABLED
    )

    update_game_information()

    update_statistics()

    save_data()

    messagebox.showinfo(
        "Game Over",
        (
            f"{reason}\n\n"
            f"The correct number was {secret_number}."
        )
    )


# =========================================================
# STATISTICS
# =========================================================

def update_statistics():

    if games_played > 0:

        win_rate = (
            games_won
            / games_played
            * 100
        )

    else:

        win_rate = 0

    statistics_label.config(
        text=(
            "📊 STATISTICS\n\n"
            f"Games Played : {games_played}\n"
            f"Games Won    : {games_won}\n"
            f"Win Rate     : {win_rate:.1f}%\n"
            f"Best Score   : {best_score}\n"
            f"Best Streak  : {best_streak}"
        )
    )

    if achievements:

        text = "🏆 ACHIEVEMENTS\n\n"

        for achievement in achievements:

            text += f"✓ {achievement}\n"

        achievements_label.config(
            text=text
        )

    else:

        achievements_label.config(
            text=(
                "🏆 ACHIEVEMENTS\n\n"
                "No achievements unlocked yet."
            )
        )


# =========================================================
# ACHIEVEMENTS
# =========================================================

def check_achievements():

    global achievements

    unlocked = None

    if (
        games_won >= 1
        and "First Win" not in achievements
    ):

        achievements.append(
            "First Win"
        )

        unlocked = "🏅 First Win"

    elif (
        best_score >= 500
        and "High Scorer" not in achievements
    ):

        achievements.append(
            "High Scorer"
        )

        unlocked = "💎 High Scorer"

    elif (
        best_streak >= 3
        and "Hot Streak" not in achievements
    ):

        achievements.append(
            "Hot Streak"
        )

        unlocked = "🔥 Hot Streak"

    elif (
        games_won >= 10
        and "Veteran" not in achievements
    ):

        achievements.append(
            "Veteran"
        )

        unlocked = "🎖️ Veteran"

    if unlocked:

        messagebox.showinfo(
            "🏆 Achievement Unlocked!",
            unlocked
        )

    save_data()


# =========================================================
# RESET STATISTICS
# =========================================================

def reset_statistics():

    global games_played
    global games_won
    global best_score
    global best_streak
    global achievements

    answer = messagebox.askyesno(
        "Reset Statistics",
        "Delete all saved statistics and achievements?"
    )

    if not answer:
        return

    games_played = 0
    games_won = 0
    best_score = 0
    best_streak = 0

    achievements = []

    save_data()

    update_statistics()

    messagebox.showinfo(
        "Reset Complete",
        "Statistics have been reset."
    )


# =========================================================
# EXIT
# =========================================================

def exit_game():

    answer = messagebox.askyesno(
        "Exit Game",
        "Are you sure you want to exit?"
    )

    if answer:

        save_data()

        root.destroy()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Number Guessing Game - V22"
)

root.geometry(
    "720x900"
)

root.resizable(
    False,
    False
)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="🎯 NUMBER GUESSING GAME",
    font=("Arial", 28, "bold")
)

title_label.pack(
    pady=(20, 2)
)


subtitle_label = tk.Label(
    root,
    text="V22 • MODERN CHALLENGE EDITION",
    font=("Arial", 11, "bold"),
    fg="#00bfff"
)

subtitle_label.pack(
    pady=(0, 12)
)


# =========================================================
# GAME MODE
# =========================================================

mode_label = tk.Label(
    root,
    text="🎮 GAME MODE",
    font=("Arial", 11, "bold")
)

mode_label.pack()


mode_variable = tk.StringVar(
    value=game_mode
)

mode_menu = tk.OptionMenu(
    root,
    mode_variable,
    "Single Player",
    "Two Player",
    command=change_mode
)

mode_menu.config(
    width=16,
    font=("Arial", 10, "bold")
)

mode_menu.pack(
    pady=5
)


# =========================================================
# PLAYER NAMES
# =========================================================

names_frame = tk.Frame(
    root
)

names_frame.pack(
    pady=5
)


player1_entry = tk.Entry(
    names_frame,
    font=("Arial", 10),
    width=18
)

player1_entry.grid(
    row=0,
    column=0,
    padx=5
)

player1_entry.insert(
    0,
    "Player 1"
)


player2_entry = tk.Entry(
    names_frame,
    font=("Arial", 10),
    width=18
)

player2_entry.grid(
    row=0,
    column=1,
    padx=5
)

player2_entry.insert(
    0,
    "Player 2"
)

player2_entry.config(
    state=tk.DISABLED
)


name_button = tk.Button(
    names_frame,
    text="SET NAMES",
    font=("Arial", 9, "bold"),
    command=set_player_names,
    bg="#008cff",
    fg="white",
    bd=0
)

name_button.grid(
    row=1,
    column=0,
    columnspan=2,
    pady=5
)


# =========================================================
# DIFFICULTY
# =========================================================

difficulty_label = tk.Label(
    root,
    text="🎚️ DIFFICULTY",
    font=("Arial", 11, "bold")
)

difficulty_label.pack()


difficulty_variable = tk.StringVar(
    value=difficulty
)

difficulty_menu = tk.OptionMenu(
    root,
    difficulty_variable,
    *DIFFICULTIES.keys(),
    command=change_difficulty
)

difficulty_menu.config(
    width=16,
    font=("Arial", 10, "bold")
)

difficulty_menu.pack(
    pady=5
)


# =========================================================
# RANGE
# =========================================================

range_frame = tk.Frame(
    root,
    padx=20,
    pady=10
)

range_frame.pack(
    pady=7
)


range_label = tk.Label(
    range_frame,
    text="Guess a number between 1 and 100",
    font=("Arial", 13, "bold")
)

range_label.pack()


# =========================================================
# PLAYER TURN
# =========================================================

player_label = tk.Label(
    root,
    text="👤 PLAYER 1'S TURN",
    font=("Arial", 13, "bold")
)

player_label.pack(
    pady=5
)


# =========================================================
# GUESS ENTRY
# =========================================================

guess_entry = tk.Entry(
    root,
    font=("Arial", 22, "bold"),
    justify="center",
    width=10
)

guess_entry.pack(
    pady=7
)


# =========================================================
# GUESS BUTTON
# =========================================================

guess_button = tk.Button(
    root,
    text="🎯 GUESS",
    font=("Arial", 12, "bold"),
    width=17,
    height=2,
    command=check_guess,
    bg="#008cff",
    fg="white",
    bd=0
)

guess_button.pack(
    pady=4
)


# =========================================================
# HINT BUTTON
# =========================================================

hint_button = tk.Button(
    root,
    text="💡 USE HINT",
    font=("Arial", 10, "bold"),
    width=17,
    height=2,
    command=use_hint,
    bg="#6f42c1",
    fg="white",
    bd=0
)

hint_button.pack(
    pady=4
)


# =========================================================
# RESULT
# =========================================================

result_label = tk.Label(
    root,
    text="🤔 A secret number has been generated.",
    font=("Arial", 14, "bold"),
    justify="center"
)

result_label.pack(
    pady=10
)


# =========================================================
# SCORE
# =========================================================

score_label = tk.Label(
    root,
    text="🏆 Score: 200",
    font=("Arial", 12, "bold"),
    fg="#ffd700"
)

score_label.pack(
    pady=2
)


# =========================================================
# ATTEMPTS
# =========================================================

attempts_label = tk.Label(
    root,
    text="🎯 Attempts: 0/10",
    font=("Arial", 12, "bold")
)

attempts_label.pack(
    pady=2
)


# =========================================================
# TIMER
# =========================================================

timer_label = tk.Label(
    root,
    text="⏱️ Time: 60s",
    font=("Arial", 12, "bold")
)

timer_label.pack(
    pady=2
)


# =========================================================
# STREAK
# =========================================================

streak_label = tk.Label(
    root,
    text="🔥 Streak: 0",
    font=("Arial", 12, "bold")
)

streak_label.pack(
    pady=2
)


# =========================================================
# STATISTICS
# =========================================================

statistics_frame = tk.Frame(
    root,
    padx=20,
    pady=7
)

statistics_frame.pack(
    pady=7
)


statistics_label = tk.Label(
    statistics_frame,
    text="",
    font=("Arial", 9, "bold"),
    justify="left"
)

statistics_label.pack()


# =========================================================
# ACHIEVEMENTS
# =========================================================

achievements_frame = tk.Frame(
    root
)

achievements_frame.pack(
    pady=2
)


achievements_label = tk.Label(
    achievements_frame,
    text="",
    font=("Arial", 9, "bold"),
    justify="left"
)

achievements_label.pack()


# =========================================================
# CONTROL BUTTONS
# =========================================================

control_frame = tk.Frame(
    root
)

control_frame.pack(
    pady=8
)


new_game_button = tk.Button(
    control_frame,
    text="🔄 NEW GAME",
    font=("Arial", 9, "bold"),
    width=13,
    height=2,
    command=new_game,
    bg="#28a745",
    fg="white",
    bd=0
)

new_game_button.grid(
    row=0,
    column=0,
    padx=3
)


theme_button = tk.Button(
    control_frame,
    text="🌓 THEME",
    font=("Arial", 9, "bold"),
    width=13,
    height=2,
    command=toggle_theme,
    bg="#6f42c1",
    fg="white",
    bd=0
)

theme_button.grid(
    row=0,
    column=1,
    padx=3
)


reset_button = tk.Button(
    control_frame,
    text="🗑️ RESET",
    font=("Arial", 9, "bold"),
    width=13,
    height=2,
    command=reset_statistics,
    bg="#fd7e14",
    fg="white",
    bd=0
)

reset_button.grid(
    row=0,
    column=2,
    padx=3
)


# =========================================================
# EXIT
# =========================================================

exit_button = tk.Button(
    root,
    text="❌ EXIT",
    font=("Arial", 9, "bold"),
    width=12,
    command=exit_game,
    bg="#dc3545",
    fg="white",
    bd=0
)

exit_button.pack(
    pady=3
)


# =========================================================
# FOOTER
# =========================================================

footer_label = tk.Label(
    root,
    text="Python • Tkinter • JSON • V22",
    font=("Arial", 8),
    fg="#888888"
)

footer_label.pack(
    side="bottom",
    pady=6
)


# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: check_guess()
)


# =========================================================
# INITIALIZE
# =========================================================

load_data()

apply_theme()

update_statistics()

new_game()


# =========================================================
# START
# =========================================================

root.mainloop()