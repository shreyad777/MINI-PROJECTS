import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# =========================================================
# NUMBER GUESSING GAME - V20
# ULTIMATE EDITION
# =========================================================

SAVE_FILE = "game_data.json"

# =========================================================
# GAME CONFIGURATION
# =========================================================

DIFFICULTIES = {
    "Easy": {
        "maximum": 50,
        "attempts": 15,
        "time": 90,
        "starting_score": 100
    },
    "Medium": {
        "maximum": 100,
        "attempts": 10,
        "time": 60,
        "starting_score": 200
    },
    "Hard": {
        "maximum": 500,
        "attempts": 7,
        "time": 45,
        "starting_score": 300
    }
}

# =========================================================
# GLOBAL VARIABLES
# =========================================================

difficulty = "Medium"

secret_number = 0
attempts_used = 0
max_attempts = 10

score = 0
best_score = 0

games_played = 0
games_won = 0

current_streak = 0
best_streak = 0

hints_used = 0
timer_seconds = 60
timer_running = False

dark_mode = True

achievements = []


# =========================================================
# DATA
# =========================================================

def load_data():
    global best_score
    global games_played
    global games_won
    global current_streak
    global best_streak
    global achievements

    if not os.path.exists(SAVE_FILE):
        return

    try:
        with open(SAVE_FILE, "r") as file:
            data = json.load(file)

        best_score = data.get("best_score", 0)
        games_played = data.get("games_played", 0)
        games_won = data.get("games_won", 0)
        current_streak = data.get("current_streak", 0)
        best_streak = data.get("best_streak", 0)
        achievements = data.get("achievements", [])

    except (json.JSONDecodeError, OSError):
        pass


def save_data():
    data = {
        "best_score": best_score,
        "games_played": games_played,
        "games_won": games_won,
        "current_streak": current_streak,
        "best_streak": best_streak,
        "achievements": achievements
    }

    try:
        with open(SAVE_FILE, "w") as file:
            json.dump(data, file, indent=4)

    except OSError:
        pass


# =========================================================
# COLORS
# =========================================================

def background_color():
    return "#141421" if dark_mode else "#eeeeee"


def card_color():
    return "#222235" if dark_mode else "#ffffff"


def text_color():
    return "#ffffff" if dark_mode else "#222222"


# =========================================================
# THEME
# =========================================================

def toggle_theme():
    global dark_mode

    dark_mode = not dark_mode

    apply_theme()


def apply_theme():

    bg = background_color()
    card = card_color()
    text = text_color()

    root.configure(bg=bg)

    title_label.config(
        bg=bg,
        fg=text
    )

    version_label.config(
        bg=bg
    )

    difficulty_label.config(
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
# ACHIEVEMENTS
# =========================================================

def check_achievements():

    global achievements

    new_achievement = None

    if games_won >= 1 and "First Win" not in achievements:
        new_achievement = "🏅 First Win"
        achievements.append("First Win")

    elif best_score >= 500 and "High Scorer" not in achievements:
        new_achievement = "💎 High Scorer"
        achievements.append("High Scorer")

    elif best_streak >= 3 and "Hot Streak" not in achievements:
        new_achievement = "🔥 Hot Streak"
        achievements.append("Hot Streak")

    elif games_won >= 10 and "Veteran" not in achievements:
        new_achievement = "🎖️ Veteran"
        achievements.append("Veteran")

    if new_achievement:
        messagebox.showinfo(
            "🏆 Achievement Unlocked!",
            new_achievement
        )

    save_data()


# =========================================================
# STATISTICS
# =========================================================

def update_statistics():

    if games_played > 0:
        win_rate = games_won / games_played * 100
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
        achievements_text = "🏆 ACHIEVEMENTS\n\n"

        for achievement in achievements:
            achievements_text += f"✓ {achievement}\n"

        achievements_label.config(
            text=achievements_text
        )

    else:
        achievements_label.config(
            text="🏆 ACHIEVEMENTS\n\nNo achievements yet."
        )


# =========================================================
# NEW GAME
# =========================================================

def new_game():

    global secret_number
    global attempts_used
    global max_attempts
    global score
    global timer_seconds
    global timer_running
    global hints_used
    global games_played

    settings = DIFFICULTIES[difficulty]

    secret_number = random.randint(1, settings["maximum"])

    attempts_used = 0
    max_attempts = settings["attempts"]

    score = settings["starting_score"]

    timer_seconds = settings["time"]

    hints_used = 0

    timer_running = True

    games_played += 1

    range_label.config(
        text=f"Guess a number between 1 and {settings['maximum']}"
    )

    result_label.config(
        text="🤔 I'm thinking of a number..."
    )

    score_label.config(
        text=f"🏆 Score: {score}"
    )

    attempts_label.config(
        text=f"🎯 Attempts: 0/{max_attempts}"
    )

    timer_label.config(
        text=f"⏱️ Time: {timer_seconds}s"
    )

    streak_label.config(
        text=f"🔥 Streak: {current_streak}"
    )

    guess_entry.config(
        state=tk.NORMAL
    )

    guess_button.config(
        state=tk.NORMAL
    )

    guess_entry.delete(0, tk.END)

    guess_entry.focus()

    update_statistics()

    save_data()

    countdown()


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

        root.after(1000, countdown)

    else:

        timer_running = False

        game_over(
            "⏰ TIME'S UP!"
        )


# =========================================================
# HINT SYSTEM
# =========================================================

def use_hint():

    global score
    global hints_used

    if not timer_running:
        return

    if hints_used >= 3:
        messagebox.showwarning(
            "Hints",
            "You have already used all 3 hints!"
        )
        return

    hints_used += 1

    score = max(0, score - 25)

    if hints_used == 1:

        if secret_number % 2 == 0:
            hint = "💡 Hint: The number is EVEN."
        else:
            hint = "💡 Hint: The number is ODD."

    elif hints_used == 2:

        if secret_number <= 50:
            hint = "💡 Hint: The number is between 1 and 50."
        else:
            hint = "💡 Hint: The number is greater than 50."

    else:

        lower = max(1, secret_number - 10)
        upper = secret_number + 10

        hint = (
            f"💡 Final Hint:\n"
            f"The number is between {lower} and {upper}."
        )

    result_label.config(
        text=hint,
        fg="#00bfff"
    )

    score_label.config(
        text=f"🏆 Score: {score}"
    )


# =========================================================
# CHECK GUESS
# =========================================================

def check_guess():

    global attempts_used
    global score
    global current_streak
    global best_streak
    global best_score
    global games_won
    global timer_running

    if not timer_running:
        return

    value = guess_entry.get().strip()

    if not value:

        result_label.config(
            text="⚠️ Enter a number first!"
        )

        return

    try:
        guess = int(value)

    except ValueError:

        result_label.config(
            text="❌ Numbers only!"
        )

        return

    maximum = DIFFICULTIES[difficulty]["maximum"]

    if guess < 1 or guess > maximum:

        result_label.config(
            text=f"⚠️ Enter a number from 1 to {maximum}!"
        )

        return

    attempts_used += 1

    # =====================================================
    # CORRECT
    # =====================================================

    if guess == secret_number:

        timer_running = False

        games_won += 1

        remaining_attempts = max_attempts - attempts_used

        score += remaining_attempts * 15

        score += timer_seconds

        score -= hints_used * 25

        score = max(10, score)

        current_streak += 1

        if current_streak > best_streak:
            best_streak = current_streak

        if score > best_score:
            best_score = score

        result_label.config(
            text=(
                f"🎉 CORRECT!\n"
                f"The number was {secret_number}!"
            ),
            fg="#00ff88"
        )

        score_label.config(
            text=f"🏆 Score: {score}"
        )

        attempts_label.config(
            text=f"🎯 Attempts: {attempts_used}/{max_attempts}"
        )

        streak_label.config(
            text=f"🔥 Streak: {current_streak}"
        )

        guess_entry.config(
            state=tk.DISABLED
        )

        guess_button.config(
            state=tk.DISABLED
        )

        update_statistics()

        save_data()

        check_achievements()

        messagebox.showinfo(
            "🎉 YOU WON!",
            (
                f"Congratulations!\n\n"
                f"Number: {secret_number}\n"
                f"Attempts: {attempts_used}\n"
                f"Score: {score}\n"
                f"🔥 Streak: {current_streak}"
            )
        )

        return

    # =====================================================
    # WRONG
    # =====================================================

    score = max(0, score - 10)

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

    score_label.config(
        text=f"🏆 Score: {score}"
    )

    attempts_label.config(
        text=f"🎯 Attempts: {attempts_used}/{max_attempts}"
    )

    guess_entry.delete(0, tk.END)

    if attempts_used >= max_attempts:

        game_over(
            "😢 NO ATTEMPTS LEFT!"
        )


# =========================================================
# GAME OVER
# =========================================================

def game_over(reason):

    global timer_running
    global current_streak

    timer_running = False

    current_streak = 0

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

    streak_label.config(
        text="🔥 Streak: 0"
    )

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
# DIFFICULTY
# =========================================================

def change_difficulty(value):

    global difficulty

    difficulty = value

    new_game()


# =========================================================
# RESET DATA
# =========================================================

def reset_statistics():

    global best_score
    global games_played
    global games_won
    global current_streak
    global best_streak
    global achievements

    answer = messagebox.askyesno(
        "Reset Everything",
        "Delete all saved statistics and achievements?"
    )

    if not answer:
        return

    best_score = 0
    games_played = 0
    games_won = 0
    current_streak = 0
    best_streak = 0
    achievements = []

    save_data()

    update_statistics()

    messagebox.showinfo(
        "Reset Complete",
        "All statistics have been reset."
    )


# =========================================================
# EXIT
# =========================================================

def exit_game():

    answer = messagebox.askyesno(
        "Exit",
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
    "Number Guessing Game - V20"
)

root.geometry(
    "650x820"
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
    font=("Arial", 26, "bold")
)

title_label.pack(
    pady=(25, 5)
)


version_label = tk.Label(
    root,
    text="V20 • ULTIMATE EDITION",
    font=("Arial", 11, "bold"),
    fg="#00bfff"
)

version_label.pack(
    pady=(0, 15)
)


# =========================================================
# DIFFICULTY
# =========================================================

difficulty_label = tk.Label(
    root,
    text="🎚️ DIFFICULTY",
    font=("Arial", 12, "bold")
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
    width=12,
    font=("Arial", 11, "bold")
)

difficulty_menu.pack(
    pady=8
)


# =========================================================
# RANGE
# =========================================================

range_frame = tk.Frame(
    root,
    padx=20,
    pady=12
)

range_frame.pack(
    pady=8
)


range_label = tk.Label(
    range_frame,
    text="Guess a number between 1 and 100",
    font=("Arial", 13, "bold")
)

range_label.pack()


# =========================================================
# ENTRY
# =========================================================

guess_entry = tk.Entry(
    root,
    font=("Arial", 22, "bold"),
    justify="center",
    width=10
)

guess_entry.pack(
    pady=12
)


# =========================================================
# GUESS BUTTON
# =========================================================

guess_button = tk.Button(
    root,
    text="🎯 GUESS",
    font=("Arial", 13, "bold"),
    width=16,
    height=2,
    command=check_guess,
    bg="#008cff",
    fg="white",
    bd=0
)

guess_button.pack(
    pady=5
)


# =========================================================
# HINT BUTTON
# =========================================================

hint_button = tk.Button(
    root,
    text="💡 USE HINT",
    font=("Arial", 11, "bold"),
    width=16,
    height=2,
    command=use_hint,
    bg="#6f42c1",
    fg="white",
    bd=0
)

hint_button.pack(
    pady=6
)


# =========================================================
# RESULT
# =========================================================

result_label = tk.Label(
    root,
    text="🤔 I'm thinking of a number...",
    font=("Arial", 15, "bold"),
    justify="center"
)

result_label.pack(
    pady=15
)


# =========================================================
# GAME INFORMATION
# =========================================================

score_label = tk.Label(
    root,
    text="🏆 Score: 200",
    font=("Arial", 13, "bold"),
    fg="#ffd700"
)

score_label.pack(
    pady=2
)


attempts_label = tk.Label(
    root,
    text="🎯 Attempts: 0/10",
    font=("Arial", 13, "bold")
)

attempts_label.pack(
    pady=2
)


timer_label = tk.Label(
    root,
    text="⏱️ Time: 60s",
    font=("Arial", 13, "bold")
)

timer_label.pack(
    pady=2
)


streak_label = tk.Label(
    root,
    text="🔥 Streak: 0",
    font=("Arial", 13, "bold")
)

streak_label.pack(
    pady=2
)


# =========================================================
# STATISTICS PANEL
# =========================================================

statistics_frame = tk.Frame(
    root,
    padx=25,
    pady=12
)

statistics_frame.pack(
    pady=10
)


statistics_label = tk.Label(
    statistics_frame,
    text="",
    font=("Arial", 10, "bold"),
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
    pady=5
)


achievements_label = tk.Label(
    achievements_frame,
    text="",
    font=("Arial", 10, "bold"),
    justify="left"
)

achievements_label.pack()


# =========================================================
# BUTTONS
# =========================================================

button_frame = tk.Frame(
    root
)

button_frame.pack(
    pady=12
)


new_game_button = tk.Button(
    button_frame,
    text="🔄 NEW GAME",
    font=("Arial", 10, "bold"),
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
    padx=4
)


theme_button = tk.Button(
    button_frame,
    text="🌓 THEME",
    font=("Arial", 10, "bold"),
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
    padx=4
)


reset_button = tk.Button(
    button_frame,
    text="🗑️ RESET",
    font=("Arial", 10, "bold"),
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
    padx=4
)


# =========================================================
# EXIT
# =========================================================

exit_button = tk.Button(
    root,
    text="❌ EXIT",
    font=("Arial", 10, "bold"),
    width=12,
    command=exit_game,
    bg="#dc3545",
    fg="white",
    bd=0
)

exit_button.pack(
    pady=5
)


# =========================================================
# FOOTER
# =========================================================

footer_label = tk.Label(
    root,
    text="Python • Tkinter • JSON • V20",
    font=("Arial", 9),
    fg="#888888"
)

footer_label.pack(
    side="bottom",
    pady=10
)


# =========================================================
# ENTER KEY
# =========================================================

root.bind(
    "<Return>",
    lambda event: check_guess()
)


# =========================================================
# INITIALIZATION
# =========================================================

load_data()

apply_theme()

update_statistics()

new_game()


# =========================================================
# START
# =========================================================

root.mainloop()